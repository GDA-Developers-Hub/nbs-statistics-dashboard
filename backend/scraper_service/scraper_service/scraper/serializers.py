from rest_framework import serializers
from .models import ScraperJob, ScrapedItem

class ScraperJobSerializer(serializers.ModelSerializer):
    """
    Serializer for ScraperJob model
    """
    duration = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = ScraperJob
        fields = [
            'id', 'job_type', 'url', 'status', 'start_time', 'end_time',
            'items_found', 'items_processed', 'items_failed', 'error_message',
            'created_at', 'updated_at', 'duration', 'success_rate'
        ]
    
    def get_duration(self, obj):
        return obj.duration
    
    def get_success_rate(self, obj):
        return obj.success_rate

class ScrapedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ScrapedItem model
    """
    job_type = serializers.ReadOnlyField(source='job.job_type')
    job_status = serializers.ReadOnlyField(source='job.status')
    category = serializers.SerializerMethodField()
    time_period = serializers.SerializerMethodField()
    columns = serializers.SerializerMethodField()
    
    class Meta:
        model = ScrapedItem
        fields = [
            'id', 'job', 'job_type', 'job_status', 'item_type', 'source_url',
            'title', 'description', 'status', 'error_message',
            'created_at', 'updated_at', 'category', 'time_period', 'columns'
        ]
    
    def get_category(self, obj):
        return obj.metadata.get('category', '') if obj.metadata else ''
    
    def get_time_period(self, obj):
        return obj.metadata.get('time_period', '') if obj.metadata else ''
    
    def get_columns(self, obj):
        return obj.metadata.get('columns', []) if obj.metadata else []

class ScrapedItemDetailSerializer(ScrapedItemSerializer):
    """
    Detailed serializer for ScrapedItem including content
    """
    
    class Meta(ScrapedItemSerializer.Meta):
        fields = ScrapedItemSerializer.Meta.fields + ['content', 'metadata']

class ScrapedItemLightSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for ScrapedItem without content field to reduce payload size.
    """
    class Meta:
        model = ScrapedItem
        fields = [
            'id', 'job', 'item_type', 
            'source_url', 'title', 'status',
            'created_at'
        ]
        read_only_fields = fields
