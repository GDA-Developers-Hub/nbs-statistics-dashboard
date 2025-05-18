from django.db import models

class Sector(models.Model):
    """
    Economic/development sector model.
    Limited to 8 main sectors as specified in requirements.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    # Optional parent sector for future extensibility
    parent_sector = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='children'
    )
    description = models.TextField(blank=True, null=True)
    # Additional metadata as JSON
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
