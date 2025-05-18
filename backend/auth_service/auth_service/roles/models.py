from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    """
    Role model for RBAC.
    
    Defines the 5 system roles as specified in the project requirements:
    1. Super Admin: Full system access, configure roles, manage users, system settings
    2. Admin: Define time-range presets, edit regions/sectors, view raw data, manage content
    3. Analyst: Create custom dashboards, export data, view all statistics
    4. Regular User: Use filters and custom date within admin limits, view published dashboards
    5. Public User: Access only to public data, limited filtering, no data export
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    # Role hierarchy level (higher number means more permissions)
    level = models.IntegerField(default=0)
    
    # Default role for new users
    is_default = models.BooleanField(default=False)
    
    # System role flag (can't be deleted)
    is_system_role = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-level', 'name']
        
    def __str__(self):
        return self.name

class RolePermission(models.Model):
    """
    Associates permissions with roles.
    Defines which permissions each role has.
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name='role_permissions'
    )
    permission_code = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['role', 'permission_code']
        
    def __str__(self):
        return f"{self.role.name} - {self.permission_code}"
