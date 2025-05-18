from django.core.management.base import BaseCommand
from django.db import transaction

from auth_service.roles.models import Role, RolePermission
from auth_service.permissions.models import Permission
from auth_service.users.models import User

class Command(BaseCommand):
    help = 'Creates default roles and permissions for the SNBS Dashboard'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating default roles and permissions...')
        
        # Create default permissions
        self.create_permissions()
        
        # Create default roles
        self.create_roles()
        
        # Assign permissions to roles
        self.assign_permissions()
        
        self.stdout.write(self.style.SUCCESS('Successfully created default roles and permissions'))

    def create_permissions(self):
        """Create default permissions"""
        default_permissions = [
            # User management permissions
            {'name': 'View User', 'code': 'view_user', 'category': 'user'},
            {'name': 'Create User', 'code': 'create_user', 'category': 'user'},
            {'name': 'Edit User', 'code': 'edit_user', 'category': 'user'},
            {'name': 'Delete User', 'code': 'delete_user', 'category': 'user'},
            
            # Role management permissions
            {'name': 'View Role', 'code': 'view_role', 'category': 'role'},
            {'name': 'Create Role', 'code': 'create_role', 'category': 'role'},
            {'name': 'Edit Role', 'code': 'edit_role', 'category': 'role'},
            {'name': 'Delete Role', 'code': 'delete_role', 'category': 'role'},
            
            # Permission management
            {'name': 'View Permission', 'code': 'view_permission', 'category': 'permission'},
            {'name': 'Create Permission', 'code': 'create_permission', 'category': 'permission'},
            {'name': 'Edit Permission', 'code': 'edit_permission', 'category': 'permission'},
            {'name': 'Delete Permission', 'code': 'delete_permission', 'category': 'permission'},
            
            # Data access permissions
            {'name': 'View Public Data', 'code': 'view_public_data', 'category': 'data'},
            {'name': 'View Data', 'code': 'view_data', 'category': 'data'},
            {'name': 'Export Data', 'code': 'export_data', 'category': 'data'},
            {'name': 'Edit Data', 'code': 'edit_data', 'category': 'data'},
            
            # Dashboard permissions
            {'name': 'View Public Dashboard', 'code': 'view_public_dashboard', 'category': 'dashboard'},
            {'name': 'View Dashboard', 'code': 'view_dashboard', 'category': 'dashboard'},
            {'name': 'Create Dashboard', 'code': 'create_dashboard', 'category': 'dashboard'},
            {'name': 'Edit Dashboard', 'code': 'edit_dashboard', 'category': 'dashboard'},
            {'name': 'Delete Dashboard', 'code': 'delete_dashboard', 'category': 'dashboard'},
            
            # Statistics permissions
            {'name': 'View Statistics', 'code': 'view_statistics', 'category': 'statistics'},
            {'name': 'Edit Statistics', 'code': 'edit_statistics', 'category': 'statistics'},
            
            # Filter permissions
            {'name': 'Use Filters', 'code': 'use_filters', 'category': 'filter'},
            {'name': 'Edit Filters', 'code': 'edit_filters', 'category': 'filter'},
            
            # System settings
            {'name': 'Manage System Settings', 'code': 'manage_system_settings', 'category': 'system'},
        ]
        
        for perm_data in default_permissions:
            Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults={
                    'name': perm_data['name'],
                    'category': perm_data['category']
                }
            )
        
        self.stdout.write(f'Created {len(default_permissions)} permissions')

    def create_roles(self):
        """Create default roles"""
        default_roles = [
            {
                'name': 'Super Admin',
                'code': User.ROLE_SUPER_ADMIN,
                'description': 'Full system access with ability to configure roles, manage users, and system settings',
                'level': 50,
                'is_system_role': True
            },
            {
                'name': 'Admin',
                'code': User.ROLE_ADMIN,
                'description': 'Ability to define time-range presets, edit regions/sectors, view raw data, manage content',
                'level': 40,
                'is_system_role': True
            },
            {
                'name': 'Analyst',
                'code': User.ROLE_ANALYST,
                'description': 'Can create custom dashboards, export data, view all statistics',
                'level': 30,
                'is_system_role': True
            },
            {
                'name': 'Regular User',
                'code': User.ROLE_USER,
                'description': 'Can use filters and custom date within admin limits, view published dashboards',
                'level': 20,
                'is_system_role': True
            },
            {
                'name': 'Public User',
                'code': User.ROLE_PUBLIC,
                'description': 'Access only to public data, limited filtering, no data export',
                'level': 10,
                'is_system_role': True,
                'is_default': True
            },
        ]
        
        for role_data in default_roles:
            Role.objects.get_or_create(
                code=role_data['code'],
                defaults={
                    'name': role_data['name'],
                    'description': role_data['description'],
                    'level': role_data['level'],
                    'is_system_role': role_data.get('is_system_role', False),
                    'is_default': role_data.get('is_default', False)
                }
            )
        
        self.stdout.write(f'Created {len(default_roles)} roles')

    def assign_permissions(self):
        """Assign permissions to roles based on their level"""
        # Clear existing role permissions
        RolePermission.objects.all().delete()
        
        # Get all permissions
        permissions = Permission.objects.all()
        
        # Get roles
        super_admin_role = Role.objects.get(code=User.ROLE_SUPER_ADMIN)
        admin_role = Role.objects.get(code=User.ROLE_ADMIN)
        analyst_role = Role.objects.get(code=User.ROLE_ANALYST)
        user_role = Role.objects.get(code=User.ROLE_USER)
        public_role = Role.objects.get(code=User.ROLE_PUBLIC)
        
        # Super Admin gets all permissions
        for perm in permissions:
            RolePermission.objects.create(role=super_admin_role, permission_code=perm.code)
        
        # Admin permissions (all except role and permission management)
        admin_excluded = [
            'create_role', 'delete_role', 
            'create_permission', 'delete_permission',
            'manage_system_settings'
        ]
        
        for perm in permissions:
            if perm.code not in admin_excluded:
                RolePermission.objects.create(role=admin_role, permission_code=perm.code)
        
        # Analyst permissions
        analyst_permissions = [
            'view_user', 'view_role', 'view_permission',
            'view_data', 'export_data',
            'view_dashboard', 'create_dashboard', 'edit_dashboard',
            'view_statistics', 'use_filters'
        ]
        
        for perm_code in analyst_permissions:
            RolePermission.objects.create(role=analyst_role, permission_code=perm_code)
        
        # Regular user permissions
        user_permissions = [
            'view_data', 'view_dashboard', 'view_statistics', 'use_filters'
        ]
        
        for perm_code in user_permissions:
            RolePermission.objects.create(role=user_role, permission_code=perm_code)
        
        # Public user permissions
        public_permissions = [
            'view_public_data', 'view_public_dashboard'
        ]
        
        for perm_code in public_permissions:
            RolePermission.objects.create(role=public_role, permission_code=perm_code)
        
        self.stdout.write('Assigned permissions to roles') 