"""
URL configuration for AUTH microservice.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="SNBS Dashboard Auth API",
        default_version=settings.API_VERSION,
        description="Authentication API for Somalia National Bureau of Statistics Dashboard",
        contact=openapi.Contact(email="info@nbs.gov.so"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API version prefix
api_prefix = f'api/{settings.API_VERSION}'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JWT token endpoints
    path(f'{api_prefix}/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path(f'{api_prefix}/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path(f'{api_prefix}/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    
    # Auth endpoints
    path(f'{api_prefix}/users/', include('auth_service.users.urls')),
    path(f'{api_prefix}/roles/', include('auth_service.roles.urls')),
    path(f'{api_prefix}/permissions/', include('auth_service.permissions.urls')),
    
    # Health check endpoint
    path('health/', include('health_check.urls')),
]
