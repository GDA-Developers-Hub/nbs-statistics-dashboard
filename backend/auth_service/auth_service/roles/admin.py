from django.contrib import admin
from .models import Role, RolePermission

class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'is_default', 'is_system_role')
    list_filter = ('is_default', 'is_system_role', 'level')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description')
        }),
        ('Role Properties', {
            'fields': ('level', 'is_default', 'is_system_role')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    inlines = [RolePermissionInline]

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission_code', 'created_at')
    list_filter = ('role',)
    search_fields = ('role__name', 'permission_code')
    readonly_fields = ('created_at',) 