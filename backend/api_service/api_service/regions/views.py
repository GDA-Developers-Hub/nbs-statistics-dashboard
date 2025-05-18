from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Region
from .serializers import RegionSerializer, RegionDetailSerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for regions data.
    Provides list and detail views for Somalia's administrative regions.
    Limited to 6 main administrative regions as specified in requirements.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_fields = ['code']
    search_fields = ['name', 'code']
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'geojson':
            return RegionDetailSerializer
        return RegionSerializer
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('regions', 86400)))  # Cache for 24 hours by default
    def list(self, request, *args, **kwargs):
        """List all regions (cached)"""
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('regions', 86400)))  # Cache for 24 hours by default
    def retrieve(self, request, *args, **kwargs):
        """Get details for a specific region (cached)"""
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(settings.CACHE_TTL.get('regions', 86400)))  # Cache for 24 hours by default
    def geojson(self, request):
        """
        Return GeoJSON for all regions for map rendering.
        This endpoint is optimized for the frontend map component.
        """
        regions = self.get_queryset()
        data = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for region in regions:
            if region.geojson:
                feature = {
                    "type": "Feature",
                    "geometry": region.geojson,
                    "properties": {
                        "id": region.id,
                        "name": region.name,
                        "code": region.code
                    }
                }
                data["features"].append(feature)
                
        return Response(data)
