from rest_framework import serializers
from .models import Role, RolePermission

class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for RolePermission model.
    """
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission_code', 'created_at']
        read_only_fields = ['id', 'created_at']

class RoleSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Role model.
    """
    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'level', 'is_default', 'is_system_role']
        read_only_fields = ['is_system_role']  # System roles cannot be modified

class RoleDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Role model with associated permissions.
    """
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'level', 'is_default', 
                 'is_system_role', 'permissions', 'created_at', 'updated_at']
        read_only_fields = ['is_system_role', 'created_at', 'updated_at']
    
    def get_permissions(self, obj):
        """Get all permissions associated with this role"""
        permissions = obj.role_permissions.all()
        return [rp.permission_code for rp in permissions]
