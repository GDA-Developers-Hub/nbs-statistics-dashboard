from rest_framework import serializers
from .models import Indicator, IndicatorValue
from api_service.regions.serializers import RegionSerializer
from api_service.sectors.serializers import SectorSerializer

class IndicatorSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the Indicator model.
    """
    class Meta:
        model = Indicator
        fields = ['id', 'name', 'code', 'unit']


class IndicatorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Indicator model.
    """
    class Meta:
        model = Indicator
        fields = [
            'id', 'name', 'code', 'unit', 'description',
            'source', 'methodology', 'metadata', 
            'created_at', 'updated_at'
        ]


class IndicatorValueSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the IndicatorValue model.
    """
    indicator_name = serializers.ReadOnlyField(source='indicator.name')
    indicator_unit = serializers.ReadOnlyField(source='indicator.unit')
    
    class Meta:
        model = IndicatorValue
        fields = [
            'id', 'indicator', 'indicator_name', 'indicator_unit',
            'value', 'date', 'change_percent'
        ]


class IndicatorValueDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the IndicatorValue model.
    Includes related indicator, region, and sector data.
    """
    indicator = IndicatorSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    
    class Meta:
        model = IndicatorValue
        fields = [
            'id', 'indicator', 'region', 'sector', 'value',
            'date', 'previous_value', 'change_percent',
            'source_url', 'source_document', 'confidence_level',
            'is_estimate', 'is_preliminary', 'metadata',
            'created_at', 'updated_at'
        ]


class KeyStatIndicatorSerializer(serializers.ModelSerializer):
    """
    Serializer for key statistical indicators table shown on the dashboard.
    Formatted for easy consumption by the frontend.
    """
    indicator_name = serializers.ReadOnlyField(source='indicator.name')
    indicator_unit = serializers.ReadOnlyField(source='indicator.unit')
    formatted_value = serializers.SerializerMethodField()
    trend = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()
    
    class Meta:
        model = IndicatorValue
        fields = [
            'id', 'indicator_name', 'formatted_value', 
            'change_percent', 'trend', 'last_updated'
        ]
    
    def get_formatted_value(self, obj):
        """Format value with unit if available"""
        if obj.indicator.unit:
            if obj.indicator.unit == '%':
                return f"{obj.value:.2f}%"
            elif obj.indicator.unit == '$':
                return f"${obj.value:,.2f}"
            else:
                return f"{obj.value} {obj.indicator.unit}"
        return f"{obj.value}"
    
    def get_trend(self, obj):
        """Return trend indicator: up, down, or neutral"""
        if obj.change_percent is None:
            return 'neutral'
        elif obj.change_percent > 0:
            return 'up'
        elif obj.change_percent < 0:
            return 'down'
        return 'neutral'
    
    def get_last_updated(self, obj):
        """Format date in human-readable format"""
        return obj.date.strftime('%b %Y')
