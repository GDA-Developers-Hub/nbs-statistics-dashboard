from django.db import models
from django.utils.translation import gettext_lazy as _

class Permission(models.Model):
    """
    Permission model for RBAC.
    
    Defines permissions that can be assigned to roles.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Group permissions by category for easier management
    category = models.CharField(max_length=50, default='general')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"
