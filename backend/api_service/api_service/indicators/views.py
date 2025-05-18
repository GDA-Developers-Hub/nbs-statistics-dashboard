from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Indicator, IndicatorValue
from .serializers import (
    IndicatorSerializer, IndicatorDetailSerializer,
    IndicatorValueSerializer, IndicatorValueDetailSerializer,
    KeyStatIndicatorSerializer
)

class IndicatorFilter(django_filters.FilterSet):
    """Filter for Indicator model"""
    class Meta:
        model = Indicator
        fields = {
            'code': ['exact', 'in'],
            'name': ['exact', 'icontains'],
        }

class IndicatorValueFilter(django_filters.FilterSet):
    """Filter for IndicatorValue model with date range support"""
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    region = django_filters.CharFilter(field_name='region__code')
    sector = django_filters.CharFilter(field_name='sector__code')
    indicator_code = django_filters.CharFilter(field_name='indicator__code')
    
    class Meta:
        model = IndicatorValue
        fields = {
            'indicator': ['exact'],
            'date': ['exact'],
        }

class IndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for indicators metadata.
    """
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filterset_class = IndicatorFilter
    search_fields = ['name', 'code', 'description']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return IndicatorDetailSerializer
        return IndicatorSerializer
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def list(self, request, *args, **kwargs):
        """List all indicators (cached)"""
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def retrieve(self, request, *args, **kwargs):
        """Get details for a specific indicator (cached)"""
        return super().retrieve(request, *args, **kwargs)

class IndicatorValueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for indicator values.
    Supports filtering by region, sector, date range, and indicator.
    """
    queryset = IndicatorValue.objects.all().select_related('indicator', 'region', 'sector')
    serializer_class = IndicatorValueSerializer
    filterset_class = IndicatorValueFilter
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list_detail':
            return IndicatorValueDetailSerializer
        elif self.action == 'key_stats':
            return KeyStatIndicatorSerializer
        return IndicatorValueSerializer
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def list(self, request, *args, **kwargs):
        """List indicator values with filtering (cached)"""
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def retrieve(self, request, *args, **kwargs):
        """Get details for a specific indicator value (cached)"""
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('key_stats', 300)))  # Cache for 5 minutes by default
    def key_stats(self, request):
        """
        Return the latest key statistical indicators.
        This endpoint is optimized for the dashboard key stats table.
        """
        # Filter parameters
        region_code = request.query_params.get('region')
        sector_code = request.query_params.get('sector')
        
        # Start with all values
        queryset = self.get_queryset()
        
        # Apply region and sector filters if provided
        if region_code:
            queryset = queryset.filter(region__code=region_code)
        if sector_code:
            queryset = queryset.filter(sector__code=sector_code)
            
        # Get the most recent value for each indicator
        # This requires a bit of raw SQL or complex query to be efficient
        from django.db.models import Max, Subquery, OuterRef
        
        # Get the latest date for each indicator
        latest_dates = IndicatorValue.objects.filter(
            indicator=OuterRef('indicator')
        ).values('indicator').annotate(
            max_date=Max('date')
        ).values('max_date')
        
        # Get the values for those latest dates
        latest_values = queryset.filter(
            date=Subquery(latest_dates)
        )
        
        # We want to focus on the key indicators specified in requirements
        key_indicator_codes = [
            'gdp_growth', 'inflation', 'foreign_investment', 
            'urban_population', 'unemployment', 'primary_enrollment'
        ]
        
        latest_values = latest_values.filter(indicator__code__in=key_indicator_codes)
        
        serializer = self.get_serializer(latest_values, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def list_detail(self, request):
        """
        Return detailed indicator values with filtering.
        Includes full related entity information.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = IndicatorValueDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = IndicatorValueDetailSerializer(queryset, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('indicators', 600)))  # Cache for 10 minutes by default
    def time_series(self, request):
        """
        Return time series data for a specific indicator.
        Optimized for charts and graphs.
        """
        indicator_code = request.query_params.get('indicator')
        region_code = request.query_params.get('region')
        sector_code = request.query_params.get('sector')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        
        if not indicator_code:
            return Response({"error": "indicator parameter is required"}, status=400)
            
        # Start with all values for this indicator
        queryset = self.get_queryset().filter(indicator__code=indicator_code)
        
        # Apply additional filters if provided
        if region_code:
            queryset = queryset.filter(region__code=region_code)
        if sector_code:
            queryset = queryset.filter(sector__code=sector_code)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
            
        # Order by date
        queryset = queryset.order_by('date')
        
        # Format response for easy chart consumption
        values = []
        indicator_name = None
        indicator_unit = None
        
        for value in queryset:
            if not indicator_name:
                indicator_name = value.indicator.name
                indicator_unit = value.indicator.unit
                
            values.append({
                'date': value.date,
                'value': value.value,
                'change_percent': value.change_percent
            })
            
        data = {
            'indicator_code': indicator_code,
            'indicator_name': indicator_name,
            'indicator_unit': indicator_unit,
            'values': values
        }
        
        return Response(data)
