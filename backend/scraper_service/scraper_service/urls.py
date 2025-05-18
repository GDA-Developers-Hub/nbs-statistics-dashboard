"""
URL configuration for SCRAPER microservice.
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
        title="SNBS Dashboard Scraper API",
        default_version=settings.API_VERSION,
        description="Scraper API for Somalia National Bureau of Statistics Dashboard",
        contact=openapi.Contact(email="info@nbs.gov.so"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Scraper endpoints
    path('api/scraper/', include('scraper_service.scraper.urls')),
    
    # Health check endpoint
    path('health/', include('health_check.urls')),
]
