from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import logging
import threading

from .models import ScraperJob, ScrapedItem
from .serializers import (
    ScraperJobSerializer,
    ScrapedItemSerializer,
    ScrapedItemLightSerializer
)
from .scrapers import StatisticsScraper, PublicationsScraper
from .message_queue import publish_scraped_items

logger = logging.getLogger(__name__)


class ScraperJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing and managing scraper jobs.
    """
    queryset = ScraperJob.objects.all()
    serializer_class = ScraperJobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['job_type', 'status']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['post'])
    def run_statistics_scraper(self, request):
        """
        Run a statistics scraper job asynchronously.
        """
        # Start scraper in background thread
        thread = threading.Thread(target=self._run_statistics_scraper)
        thread.daemon = True
        thread.start()
        
        return Response({
            'message': 'Statistics scraper job started successfully',
            'status': 'running'
        })
    
    @action(detail=False, methods=['post'])
    def run_publications_scraper(self, request):
        """
        Run a publications scraper job asynchronously.
        """
        # Start scraper in background thread
        thread = threading.Thread(target=self._run_publications_scraper)
        thread.daemon = True
        thread.start()
        
        return Response({
            'message': 'Publications scraper job started successfully',
            'status': 'running'
        })
    
    def _run_statistics_scraper(self):
        """
        Run statistics scraper in background thread.
        """
        try:
            scraper = StatisticsScraper()
            scraper.run()
        except Exception as e:
            logger.exception(f"Error running statistics scraper: {str(e)}")
    
    def _run_publications_scraper(self):
        """
        Run publications scraper in background thread.
        """
        try:
            scraper = PublicationsScraper()
            scraper.run()
        except Exception as e:
            logger.exception(f"Error running publications scraper: {str(e)}")
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """
        Get all scraped items for a specific job.
        """
        job = self.get_object()
        items = job.items.all()
        
        # Use lightweight serializer by default to reduce payload size
        lightweight = request.query_params.get('lightweight', 'true').lower() == 'true'
        
        if lightweight:
            serializer = ScrapedItemLightSerializer(items, many=True)
        else:
            serializer = ScrapedItemSerializer(items, many=True)
            
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish_items(self, request, pk=None):
        """
        Publish pending scraped items for a job to the message queue.
        """
        job = self.get_object()
        
        # Get pending items
        items = job.items.filter(status=ScrapedItem.STATUS_PENDING)
        
        if not items:
            return Response({
                'message': 'No pending items found for this job',
                'count': 0
            })
        
        try:
            # Publish items to queue
            count = publish_scraped_items(items)
            
            return Response({
                'message': f'Successfully published {count} items to message queue',
                'count': count
            })
            
        except Exception as e:
            logger.exception(f"Error publishing items: {str(e)}")
            return Response({
                'message': f'Error publishing items: {str(e)}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScrapedItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing scraped items.
    """
    queryset = ScrapedItem.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['job', 'item_type', 'status']
    search_fields = ['title', 'description', 'source_url']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        # Use lightweight serializer for list view
        if self.action == 'list':
            return ScrapedItemLightSerializer
        return ScrapedItemSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Publish a specific item to the message queue.
        """
        item = self.get_object()
        
        if item.status != ScrapedItem.STATUS_PENDING:
            return Response({
                'message': f'Item is not in pending status (current status: {item.status})',
                'status': item.status
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Publish to queue
            count = publish_scraped_items(ScrapedItem.objects.filter(id=item.id))
            
            if count > 0:
                return Response({
                    'message': 'Item successfully published to message queue',
                    'message_id': item.message_id,
                    'queue_name': item.queue_name
                })
            else:
                return Response({
                    'message': 'Failed to publish item to message queue',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.exception(f"Error publishing item: {str(e)}")
            return Response({
                'message': f'Error publishing item: {str(e)}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
