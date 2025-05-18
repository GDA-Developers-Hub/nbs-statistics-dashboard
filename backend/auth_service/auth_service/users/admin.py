from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserRegionAccess, UserSectorAccess, UserSession

class UserRegionAccessInline(admin.TabularInline):
    model = UserRegionAccess
    extra = 1

class UserSectorAccessInline(admin.TabularInline):
    model = UserSectorAccess
    extra = 1

class UserSessionInline(admin.TabularInline):
    model = UserSession
    extra = 0
    readonly_fields = ('session_key', 'ip_address', 'user_agent', 'created_at', 'last_activity')
    can_delete = False
    max_num = 5
    show_change_link = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name', 'organization')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'organization', 'position', 'phone_number')}),
        (_('Access'), {'fields': ('role', 'two_factor_enabled', 'language_preference')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_password_change')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'full_name'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined', 'last_password_change')
    inlines = [UserRegionAccessInline, UserSectorAccessInline, UserSessionInline]

@admin.register(UserRegionAccess)
class UserRegionAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'region_code', 'access_level', 'created_at')
    list_filter = ('access_level', 'region_code')
    search_fields = ('user__email', 'region_code')
    
@admin.register(UserSectorAccess)
class UserSectorAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'sector_code', 'access_level', 'created_at')
    list_filter = ('access_level', 'sector_code')
    search_fields = ('user__email', 'sector_code')
    
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'is_active', 'created_at', 'last_activity')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'ip_address', 'user_agent')
    readonly_fields = ('session_key', 'ip_address', 'user_agent', 'created_at', 'last_activity') 