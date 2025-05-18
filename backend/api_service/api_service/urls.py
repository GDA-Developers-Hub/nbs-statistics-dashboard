"""
URL configuration for API microservice.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="SNBS Dashboard API",
        default_version=settings.API_VERSION,
        description="API for Somalia National Bureau of Statistics Dashboard",
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
    
    # API endpoints
    path(f'{api_prefix}/regions/', include('api_service.regions.urls')),
    path(f'{api_prefix}/sectors/', include('api_service.sectors.urls')),
    path(f'{api_prefix}/indicators/', include('api_service.indicators.urls')),
    path(f'{api_prefix}/statistics/', include('api_service.statistics.urls')),
    
    # Health check endpoint
    path('health/', include('health_check.urls')),
]
