from django.db import models

class ScraperJob(models.Model):
    """
    Model to track scraper job execution history.
    """
    TYPE_STATISTICS = 'statistics'
    TYPE_PUBLICATIONS = 'publications'
    
    JOB_TYPES = [
        (TYPE_STATISTICS, 'Statistics Pages'),
        (TYPE_PUBLICATIONS, 'Publications/PDFs'),
    ]
    
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    ]
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    url = models.URLField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Job details
    items_found = models.IntegerField(default=0)
    items_processed = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)
    
    # Error details
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.job_type} job - {self.start_time} - {self.status}"
        
    @property
    def duration(self):
        """Calculate job duration in seconds"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
        
    @property
    def success_rate(self):
        """Calculate job success rate as percentage"""
        if self.items_found > 0:
            return (self.items_processed / self.items_found) * 100
        return 0

class ScrapedItem(models.Model):
    """
    Model to track individual items scraped from the website.
    """
    TYPE_HTML_TABLE = 'html_table'
    TYPE_PDF_TABLE = 'pdf_table'
    TYPE_PDF_TEXT = 'pdf_text'
    
    ITEM_TYPES = [
        (TYPE_HTML_TABLE, 'HTML Table'),
        (TYPE_PDF_TABLE, 'PDF Table'),
        (TYPE_PDF_TEXT, 'PDF Text'),
    ]
    
    STATUS_PENDING = 'pending'
    STATUS_PROCESSED = 'processed'
    STATUS_FAILED = 'failed'
    STATUS_INVALID = 'invalid'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending ETL Processing'),
        (STATUS_PROCESSED, 'Processed'),
        (STATUS_FAILED, 'Failed to Process'),
        (STATUS_INVALID, 'Invalid Data'),
    ]
    
    job = models.ForeignKey(ScraperJob, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    source_url = models.URLField(max_length=500)
    
    # For PDF items
    page_number = models.IntegerField(null=True, blank=True)
    table_number = models.IntegerField(null=True, blank=True)
    
    # Content details
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Raw data and metadata
    content = models.JSONField()
    metadata = models.JSONField(default=dict, blank=True)
    
    # Processing status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    error_message = models.TextField(blank=True, null=True)
    
    # Message queue details
    message_id = models.CharField(max_length=100, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['job', 'created_at']
        
    def __str__(self):
        if self.title:
            return f"{self.item_type} - {self.title}"
        return f"{self.item_type} from {self.source_url}"
