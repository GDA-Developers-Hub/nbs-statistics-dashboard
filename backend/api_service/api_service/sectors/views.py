from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Sector
from .serializers import SectorSerializer, SectorDetailSerializer

class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for sectors data.
    Provides list and detail views for Somalia's economic/development sectors.
    Limited to 8 main sectors as specified in requirements.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    filterset_fields = ['code']
    search_fields = ['name', 'code', 'description']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SectorDetailSerializer
        return SectorSerializer
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('sectors', 86400)))  # Cache for 24 hours by default
    def list(self, request, *args, **kwargs):
        """List all sectors (cached)"""
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.CACHE_TTL.get('sectors', 86400)))  # Cache for 24 hours by default
    def retrieve(self, request, *args, **kwargs):
        """Get details for a specific sector (cached)"""
        return super().retrieve(request, *args, **kwargs)
