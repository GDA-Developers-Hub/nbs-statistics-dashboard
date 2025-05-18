from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndicatorViewSet, IndicatorValueViewSet

router = DefaultRouter()
router.register('metadata', IndicatorViewSet)
router.register('', IndicatorValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('key-stats/', IndicatorValueViewSet.as_view({'get': 'key_stats'}), name='key-stats'),
]
