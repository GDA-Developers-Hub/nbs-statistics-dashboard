from django.contrib import admin
from django.utils.html import format_html
from .models import ScraperJob, ScrapedItem
import json
from datetime import datetime

@admin.register(ScraperJob)
class ScraperJobAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScraperJob model.
    """
    list_display = ('id', 'job_type', 'status', 'formatted_start_time', 'formatted_end_time', 'duration_display', 'items_found', 'items_processed', 'success_rate_display')
    list_filter = ('job_type', 'status', 'start_time')
    search_fields = ('url', 'error_message')
    readonly_fields = ('duration_display', 'success_rate_display', 'formatted_start_time', 'formatted_end_time')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job_type', 'url', 'status')
        }),
        ('Progress', {
            'fields': ('items_found', 'items_processed', 'items_failed', 'success_rate_display')
        }),
        ('Timing', {
            'fields': ('formatted_start_time', 'formatted_end_time', 'duration_display')
        }),
        ('Error Details', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_start_time(self, obj):
        if obj.start_time:
            return obj.start_time.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"
    formatted_start_time.short_description = "Start Time"
    
    def formatted_end_time(self, obj):
        if obj.end_time:
            return obj.end_time.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"
    formatted_end_time.short_description = "End Time"
    
    def duration_display(self, obj):
        if obj.duration is not None:
            seconds = obj.duration
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            elif minutes > 0:
                return f"{int(minutes)}m {int(seconds)}s"
            return f"{int(seconds)}s"
        return "N/A"
    duration_display.short_description = "Duration"
    
    def success_rate_display(self, obj):
        if obj.success_rate is not None:
            color = "green"
            if obj.success_rate < 50:
                color = "red"
            elif obj.success_rate < 80:
                color = "orange"
            return format_html('<span style="color: {}; font-weight: bold;">{:.1f}%</span>', color, obj.success_rate)
        return "N/A"
    success_rate_display.short_description = "Success Rate"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-start_time')

class ScrapedItemInline(admin.TabularInline):
    model = ScrapedItem
    fields = ('title', 'item_type', 'status')
    readonly_fields = fields
    extra = 0
    max_num = 10
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScrapedItem model.
    """
    list_display = ('id', 'title', 'item_type', 'job_link', 'category', 'status', 'formatted_created_at')
    list_filter = ('item_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'source_url')
    readonly_fields = ('job', 'job_link', 'content_formatted', 'metadata_formatted', 'category', 'time_period', 'formatted_created_at')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('title', 'description', 'job_link', 'item_type', 'source_url')
        }),
        ('Metadata', {
            'fields': ('category', 'time_period', 'metadata_formatted'),
        }),
        ('Content', {
            'fields': ('content_formatted',),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('status', 'error_message', 'formatted_created_at')
        }),
    )
    
    def formatted_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"
    formatted_created_at.short_description = "Created At"
    
    def job_link(self, obj):
        if obj.job:
            url = f"/admin/scraper/scraperjob/{obj.job.id}/change/"
            return format_html('<a href="{}">{} ({})</a>', url, obj.job.job_type, obj.job.id)
        return "-"
    job_link.short_description = "Job"
    
    def category(self, obj):
        category = obj.metadata.get('category', '-') if obj.metadata else '-'
        return format_html('<span style="font-weight: bold;">{}</span>', category)
    category.short_description = "Category"
    
    def time_period(self, obj):
        return obj.metadata.get('time_period', '-') if obj.metadata else '-'
    time_period.short_description = "Time Period"
    
    def content_formatted(self, obj):
        if not obj.content:
            return "-"
        
        try:
            if isinstance(obj.content, str):
                content = json.loads(obj.content)
            else:
                content = obj.content
                
            formatted = json.dumps(content, indent=4, sort_keys=True)
            return format_html('<pre style="max-height: 500px; overflow-y: auto; background-color: #f8f9fa; padding: 10px; border-radius: 4px;">{}</pre>', formatted)
        except Exception as e:
            return format_html('<div>Error formatting content: {}</div><pre>{}</pre>', str(e), obj.content)
    content_formatted.short_description = "Content"
    
    def metadata_formatted(self, obj):
        if not obj.metadata:
            return "-"
            
        try:
            formatted = json.dumps(obj.metadata, indent=4, sort_keys=True)
            return format_html('<pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px;">{}</pre>', formatted)
        except Exception as e:
            return format_html('<div>Error formatting metadata: {}</div><pre>{}</pre>', str(e), obj.metadata)
    metadata_formatted.short_description = "Metadata"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('job').order_by('-created_at')
