from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Permission
from .serializers import PermissionSerializer, PermissionDetailSerializer
from auth_service.roles.models import Role, RolePermission

User = get_user_model()

class IsSuperAdminOnly(permissions.BasePermission):
    """
    Permission to allow only super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SUPER_ADMIN

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permission to allow only admin and super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.ROLE_ADMIN, User.ROLE_SUPER_ADMIN
        ]

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for permissions management.
    
    Super Admin: Full access to view, create, update and delete permissions
    Admin: Read-only access to permissions
    Others: No access
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    
    def get_permissions(self):
        """
        Define permissions based on action:
        - list, retrieve: Admin or Super Admin
        - create, update, partial_update, destroy: Super Admin only
        """
        if self.action in ['list', 'retrieve']:
            # Admin users can view permissions but not modify them
            permission_classes = [IsAdminOrSuperAdmin]
        else:
            # Only super admins can modify permissions
            permission_classes = [IsSuperAdminOnly]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return PermissionDetailSerializer
        return PermissionSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        List all permission categories.
        """
        categories = Permission.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Group permissions by category.
        """
        categories = Permission.objects.values_list('category', flat=True).distinct()
        result = {}
        
        for category in categories:
            permissions = Permission.objects.filter(category=category)
            serializer = PermissionSerializer(permissions, many=True)
            result[category] = serializer.data
            
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def my_permissions(self, request):
        """
        List permissions of the current user based on their role.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
            
        user_role = request.user.role
        
        # Find the Role object that matches the user's role
        try:
            role = Role.objects.get(code=user_role)
        except Role.DoesNotExist:
            return Response({"detail": "Role not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all permissions for this role
        role_permissions = RolePermission.objects.filter(role=role)
        permission_codes = [rp.permission_code for rp in role_permissions]
        
        # Get permission details
        permissions = Permission.objects.filter(code__in=permission_codes)
        serializer = PermissionSerializer(permissions, many=True)
        
        return Response(serializer.data)
