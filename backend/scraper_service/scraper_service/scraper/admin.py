from django.contrib import admin
from .models import ScraperJob, ScrapedItem

@admin.register(ScraperJob)
class ScraperJobAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScraperJob model.
    """
    list_display = (
        'id', 'job_type', 'status', 'start_time', 
        'items_found', 'items_processed', 'items_failed', 'success_rate'
    )
    list_filter = ('job_type', 'status')
    search_fields = ('url',)
    readonly_fields = (
        'job_type', 'url', 'status', 'start_time', 'end_time',
        'items_found', 'items_processed', 'items_failed',
        'error_message', 'created_at', 'updated_at'
    )
    fieldsets = (
        ('Job Information', {
            'fields': ('job_type', 'url', 'status')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'created_at', 'updated_at')
        }),
        ('Results', {
            'fields': ('items_found', 'items_processed', 'items_failed')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Only allow deleting old jobs to keep the database clean
        return True

@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScrapedItem model.
    """
    list_display = (
        'id', 'job', 'item_type', 'title', 'status',
        'page_number', 'table_number', 'created_at'
    )
    list_filter = ('item_type', 'status')
    search_fields = ('title', 'source_url')
    readonly_fields = (
        'job', 'item_type', 'source_url', 'page_number',
        'table_number', 'title', 'description', 'content',
        'metadata', 'status', 'error_message', 'message_id',
        'queue_name', 'created_at', 'updated_at'
    )
    fieldsets = (
        ('Item Information', {
            'fields': ('job', 'item_type', 'source_url')
        }),
        ('Content Details', {
            'fields': ('title', 'description')
        }),
        ('PDF-specific', {
            'fields': ('page_number', 'table_number'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('content', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Processing Status', {
            'fields': ('status', 'error_message', 'message_id', 'queue_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deleting to clean up the database
        return True
