from rest_framework import serializers
from .models import Region

class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Region model.
    Provides basic information about a region.
    """
    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'center_lat', 'center_lng']
        
class RegionDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Region model.
    Includes GeoJSON data for map rendering.
    """
    class Meta:
        model = Region
        fields = [
            'id', 'name', 'code', 'parent_region', 
            'geojson', 'bbox_north', 'bbox_south', 'bbox_east', 'bbox_west',
            'center_lat', 'center_lng', 'metadata', 'created_at', 'updated_at'
        ]
