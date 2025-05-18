from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectorViewSet

router = DefaultRouter()
router.register('', SectorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
