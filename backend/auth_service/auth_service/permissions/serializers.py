from rest_framework import serializers
from .models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model.
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'code', 'description', 'category']
        read_only_fields = ['id']

class PermissionDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Permission model.
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'code', 'description', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
