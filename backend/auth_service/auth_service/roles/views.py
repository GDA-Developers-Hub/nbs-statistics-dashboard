from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Role, RolePermission
from .serializers import RoleSerializer, RoleDetailSerializer, RolePermissionSerializer

User = get_user_model()

class IsSuperAdminOnly(permissions.BasePermission):
    """
    Permission to allow only super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SUPER_ADMIN

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for roles management.
    
    Super Admin: Full access to view, create, update and delete roles
    Admin: Read-only access to roles
    Others: No access
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    def get_permissions(self):
        """
        Define permissions based on action:
        - list, retrieve: Admin or Super Admin
        - create, update, partial_update, destroy: Super Admin only
        """
        if self.action in ['list', 'retrieve']:
            # Admin users can view roles but not modify them
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only super admins can modify roles
            permission_classes = [IsSuperAdminOnly]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return RoleDetailSerializer
        return RoleSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to check if user is at least Admin.
        """
        if not request.user.is_admin_user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method to check if user is at least Admin.
        """
        if not request.user.is_admin_user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        """
        Add a permission to a role.
        """
        role = self.get_object()
        permission_code = request.data.get('permission_code')
        
        if not permission_code:
            return Response(
                {"error": "permission_code is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if permission already exists
        if RolePermission.objects.filter(role=role, permission_code=permission_code).exists():
            return Response(
                {"error": "Permission already assigned to this role"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new permission assignment
        role_permission = RolePermission.objects.create(
            role=role,
            permission_code=permission_code
        )
        
        serializer = RolePermissionSerializer(role_permission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def remove_permission(self, request, pk=None):
        """
        Remove a permission from a role.
        """
        role = self.get_object()
        permission_code = request.data.get('permission_code')
        
        if not permission_code:
            return Response(
                {"error": "permission_code is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to find and delete the permission
        try:
            role_permission = RolePermission.objects.get(
                role=role,
                permission_code=permission_code
            )
            role_permission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RolePermission.DoesNotExist:
            return Response(
                {"error": "Permission not found for this role"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """
        List all permissions for a role.
        """
        role = self.get_object()
        role_permissions = RolePermission.objects.filter(role=role)
        serializer = RolePermissionSerializer(role_permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_permissions(self, request, pk=None):
        """
        Set all permissions for a role (replaces existing).
        """
        role = self.get_object()
        permission_codes = request.data.get('permission_codes', [])
        
        if not isinstance(permission_codes, list):
            return Response(
                {"error": "permission_codes must be a list"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete existing permissions
        RolePermission.objects.filter(role=role).delete()
        
        # Create new permissions
        new_permissions = []
        for permission_code in permission_codes:
            new_permissions.append(RolePermission(
                role=role,
                permission_code=permission_code
            ))
        
        # Bulk create
        if new_permissions:
            RolePermission.objects.bulk_create(new_permissions)
        
        # Return updated role with permissions
        serializer = RoleDetailSerializer(role)
        return Response(serializer.data)
