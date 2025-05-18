from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import logging
import threading
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from django.core.cache import cache
import json
import pandas as pd
from datetime import datetime, timedelta

from .models import ScraperJob, ScrapedItem
from .serializers import (
    ScraperJobSerializer,
    ScrapedItemSerializer,
    ScrapedItemLightSerializer
)
from .scrapers import StatisticsScraper, PublicationsScraper
from .message_queue import publish_scraped_items
from .realtime import real_time_manager

logger = logging.getLogger(__name__)


class ScraperJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing and managing scraper jobs.
    """
    queryset = ScraperJob.objects.all().order_by('-start_time')
    serializer_class = ScraperJobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['job_type', 'status']
    ordering_fields = ['start_time', 'end_time']
    
    @action(detail=False, methods=['post'])
    def run_scraper(self, request):
        """
        Run the Somalia stats scraper with specified categories
        """
        categories = request.data.get('categories', [])
        
        if categories:
            args = ['--categories'] + categories
        else:
            args = []
            
        try:
            # Run the scraper in the background
            call_command('run_somalia_scraper_test', *args)
            return Response({'status': 'success', 'message': 'Scraper job started'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)


class ScrapedItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing scraped items.
    """
    queryset = ScrapedItem.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['item_type', 'status', 'job__job_type', 'metadata__category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_permissions(self):
        """
        Allow unauthenticated access to public endpoints.
        """
        if self.action in ['list', 'retrieve', 'data', 'categories']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        # Use lightweight serializer for list view
        if self.action == 'list':
            return ScrapedItemLightSerializer
        return ScrapedItemSerializer
    
    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """
        Get the data from a scraped item in a standardized format
        """
        item = self.get_object()
        
        try:
            # Parse the content as a pandas DataFrame
            if isinstance(item.content, str):
                content = json.loads(item.content)
            else:
                content = item.content
                
            if 'schema' in content and 'data' in content:
                # The content is already in table format
                df = pd.DataFrame(content['data'])
            else:
                # Try to convert to DataFrame
                df = pd.DataFrame(content)
                
            # Get metadata
            metadata = item.metadata or {}
            category = metadata.get('category', '')
            time_period = metadata.get('time_period', '')
            
            # Convert DataFrame to JSON
            data = df.to_dict(orient='records')
            
            # Get column information
            columns = []
            for col in df.columns:
                col_type = str(df[col].dtype)
                columns.append({
                    'name': col,
                    'type': col_type
                })
            
            # Return standardized response
            return Response({
                'id': item.id,
                'title': item.title,
                'category': category,
                'time_period': time_period,
                'columns': columns,
                'data': data
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error parsing data: {str(e)}',
                'content': item.content
            }, status=400)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Get all available data categories
        """
        categories = ScrapedItem.objects.values_list('metadata__category', flat=True).distinct()
        categories = [c for c in categories if c]
        return Response(sorted(categories))


@require_http_methods(["GET"])
def latest_statistics(request):
    """
    Get the latest statistics for the dashboard
    """
    try:
        # Try to get from cache first for better performance
        cached_data = cache.get('latest_somalia_data')
        if cached_data:
            return JsonResponse(cached_data)
            
        # If not in cache, get from database
        result = real_time_manager.get_latest_data()
        
        # Cache for 5 minutes
        cache.set('latest_somalia_data', result, 300)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to trigger a scrape
def trigger_realtime_scrape(request):
    """
    Trigger a real-time scrape for the specified categories.
    
    Example:
    {
        "categories": ["demographics", "economy", "inflation"],
        "force": true
    }
    """
    try:
        # Extract parameters
        categories = request.data.get('categories')
        force = request.data.get('force', False)
        
        # Trigger the scrape
        result = real_time_manager.trigger_scrape(categories, force)
        
        return Response(result)
        
    except Exception as e:
        logger.exception(f"Error triggering real-time scrape: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def realtime_data(request, category=None):
    """
    Get real-time data for a specific category or all categories.
    
    This endpoint:
    1. Returns the latest cached data
    2. Optionally triggers a background scrape if data is stale
    """
    try:
        # Try to get from cache first
        cache_key = f'realtime_data_{category}' if category else 'latest_somalia_data'
        cached_data = cache.get(cache_key)
        
        # Check if we need to trigger a scrape
        auto_update = request.query_params.get('auto_update', 'false').lower() == 'true'
        
        if auto_update:
            # Check if data is stale (more than 5 minutes old)
            is_stale = True
            if cached_data and 'last_updated' in cached_data:
                last_updated = datetime.fromisoformat(cached_data['last_updated'])
                is_stale = (datetime.now() - last_updated) > timedelta(minutes=5)
            
            # Trigger background scrape if stale
            if is_stale:
                categories_to_scrape = [category] if category else None
                real_time_manager.trigger_scrape(categories_to_scrape)
        
        # If we have cached data, return it immediately
        if cached_data:
            return Response(cached_data)
        
        # Otherwise, get fresh data
        result = real_time_manager.get_latest_data(category)
        
        # Cache the result
        cache.set(cache_key, result, 300)  # Cache for 5 minutes
        
        return Response(result)
        
    except Exception as e:
        logger.exception(f"Error getting real-time data: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
