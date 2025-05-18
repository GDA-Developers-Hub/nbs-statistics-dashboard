from rest_framework import serializers
from .models import Sector

class SectorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sector model.
    Provides basic information about a sector.
    """
    class Meta:
        model = Sector
        fields = ['id', 'name', 'code']
        
class SectorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Sector model.
    Includes description and metadata.
    """
    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'code', 'parent_sector',
            'description', 'metadata', 'created_at', 'updated_at'
        ]
