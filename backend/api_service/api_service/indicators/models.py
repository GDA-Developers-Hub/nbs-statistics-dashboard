from django.db import models
from api_service.regions.models import Region
from api_service.sectors.models import Sector

class Indicator(models.Model):
    """
    Statistical indicator definition model.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    methodology = models.TextField(null=True, blank=True)
    
    # Metadata as JSON for additional properties
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class IndicatorValue(models.Model):
    """
    Individual indicator value model.
    Associates a value with an indicator for a specific region, sector, and date.
    """
    indicator = models.ForeignKey(
        Indicator, 
        on_delete=models.CASCADE,
        related_name='values'
    )
    region = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE,
        related_name='indicator_values',
        null=True, 
        blank=True
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name='indicator_values',
        null=True,
        blank=True
    )
    value = models.FloatField()
    date = models.DateField()
    
    # Previous value for calculating changes
    previous_value = models.FloatField(null=True, blank=True)
    # Change as percentage
    change_percent = models.FloatField(null=True, blank=True)
    
    # Data source details
    source_url = models.URLField(max_length=500, null=True, blank=True)
    source_document = models.CharField(max_length=255, null=True, blank=True)
    
    # Data quality and confidence metrics
    confidence_level = models.FloatField(null=True, blank=True)  # 0-1 scale
    is_estimate = models.BooleanField(default=False)
    is_preliminary = models.BooleanField(default=False)
    
    # Additional metadata as JSON
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'indicator__name']
        # Ensure uniqueness for indicator-region-sector-date combination
        unique_together = ['indicator', 'region', 'sector', 'date']
        
    def __str__(self):
        region_name = self.region.name if self.region else "National"
        sector_name = self.sector.name if self.sector else "All Sectors"
        return f"{self.indicator.name} - {region_name} - {sector_name} - {self.date}"
        
    def save(self, *args, **kwargs):
        """
        Override save method to calculate change_percent if previous_value exists
        """
        if self.previous_value is not None and self.previous_value != 0:
            self.change_percent = ((self.value - self.previous_value) / self.previous_value) * 100
        super().save(*args, **kwargs)
