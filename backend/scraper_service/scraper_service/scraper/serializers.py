from rest_framework import serializers
from .models import ScraperJob, ScrapedItem

class ScraperJobSerializer(serializers.ModelSerializer):
    """
    Serializer for the ScraperJob model.
    """
    success_rate = serializers.FloatField(read_only=True)
    duration = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ScraperJob
        fields = [
            'id', 'job_type', 'url', 'status', 
            'start_time', 'end_time', 'items_found',
            'items_processed', 'items_failed', 
            'success_rate', 'duration',
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class ScrapedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ScrapedItem model.
    """
    job_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ScrapedItem
        fields = [
            'id', 'job', 'job_details', 'item_type', 
            'source_url', 'page_number', 'table_number',
            'title', 'description', 'content', 'metadata',
            'status', 'error_message', 'message_id', 'queue_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields
    
    def get_job_details(self, obj):
        """
        Return minimal details about the related job.
        """
        return {
            'id': obj.job.id,
            'job_type': obj.job.job_type,
            'status': obj.job.status
        }

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
