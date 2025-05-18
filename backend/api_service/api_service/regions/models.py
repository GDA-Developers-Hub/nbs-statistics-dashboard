from django.contrib.gis.db import models

class Region(models.Model):
    """
    Somalia administrative region model.
    Limited to 6 main administrative regions as specified in requirements.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    # Optional parent region for future extensibility
    parent_region = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='children'
    )
    # GeoJSON data for map rendering
    geojson = models.TextField(null=True, blank=True)
    # Bounding box coordinates
    bbox_north = models.FloatField(null=True, blank=True)
    bbox_south = models.FloatField(null=True, blank=True)
    bbox_east = models.FloatField(null=True, blank=True)
    bbox_west = models.FloatField(null=True, blank=True)
    # Geographic center point
    center_lat = models.FloatField(null=True, blank=True)
    center_lng = models.FloatField(null=True, blank=True)
    # Additional metadata as JSON
    metadata = models.JSONField(default=dict, blank=True)
    
    # Geographic polygon for the region
    geometry = models.MultiPolygonField(srid=4326, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

    @property
    def display_name(self):
        """Return formatted display name for the region"""
        return self.name
