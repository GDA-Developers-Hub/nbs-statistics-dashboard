from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from auth_service.roles.models import Role, RolePermission

User = get_user_model()

class RoleBasedPermissionBackend(ModelBackend):
    """
    Custom authentication backend that supports Role-Based Access Control (RBAC).
    
    This backend provides:
    1. Standard authentication via email and password
    2. Permission checks based on user roles
    3. Role hierarchy (higher level roles have all permissions of lower level roles)
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user by email and password.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user has permission based on their role.
        """
        # Anonymous users have no permissions
        if not user_obj.is_authenticated:
            return False
        
        # Superusers have all permissions
        if user_obj.is_superuser:
            return True
        
        # Get user's role
        user_role_code = user_obj.role
        
        try:
            # Find the role object
            role = Role.objects.get(code=user_role_code)
            
            # Check if the user has the specific permission
            has_permission = RolePermission.objects.filter(
                role=role,
                permission_code=perm
            ).exists()
            
            if has_permission:
                return True
            
            # Check if the user's role inherits from other roles with this permission
            # This implements role hierarchy - higher level roles inherit permissions from lower levels
            if perm == 'view_data':
                # All authenticated users can view data, with varying levels of access
                return True
                
            # Super Admin has all permissions
            if user_role_code == User.ROLE_SUPER_ADMIN:
                return True
                
            # Admin has most permissions except super admin specific ones
            if user_role_code == User.ROLE_ADMIN:
                # List of permissions that only super admin should have
                super_admin_only = [
                    'delete_role', 'create_role', 
                    'delete_permission', 'create_permission',
                    'manage_system_settings'
                ]
                
                if perm not in super_admin_only:
                    return True
            
            # Analyst has limited permissions
            if user_role_code == User.ROLE_ANALYST:
                analyst_permissions = [
                    'view_data', 'export_data', 
                    'create_dashboard', 'view_dashboard',
                    'view_statistics'
                ]
                
                if perm in analyst_permissions:
                    return True
            
            # Regular user has basic viewing permissions
            if user_role_code == User.ROLE_USER:
                user_permissions = [
                    'view_data', 'view_dashboard',
                    'view_statistics', 'use_filters'
                ]
                
                if perm in user_permissions:
                    return True
            
            # Public user has minimal permissions
            if user_role_code == User.ROLE_PUBLIC:
                public_permissions = [
                    'view_public_data', 
                    'view_public_dashboard'
                ]
                
                if perm in public_permissions:
                    return True
            
            return False
            
        except Role.DoesNotExist:
            return False
    
    def has_module_perms(self, user_obj, app_label):
        """
        Check if user has any permissions for the app.
        """
        # Superusers have all permissions
        if user_obj.is_superuser:
            return True
            
        # Super Admins and Admins have access to all modules
        if user_obj.role in [User.ROLE_SUPER_ADMIN, User.ROLE_ADMIN]:
            return True
            
        # Access control for other roles based on app
        if app_label == 'statistics' or app_label == 'dashboard':
            # All users can access statistics and dashboard modules
            return True
            
        if app_label == 'api' and user_obj.is_authenticated:
            # All authenticated users can access the API
            return True
            
        if app_label == 'auth' and user_obj.is_authenticated:
            # All authenticated users can access their own auth endpoints
            return True
            
        if app_label == 'scraper' or app_label == 'etl':
            # Only admin users can access scraper and ETL modules
            return user_obj.role in [User.ROLE_SUPER_ADMIN, User.ROLE_ADMIN]
            
        return False
