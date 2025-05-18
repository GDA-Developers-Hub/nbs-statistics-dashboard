from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScraperJobViewSet, ScrapedItemViewSet

router = DefaultRouter()
router.register(r'jobs', ScraperJobViewSet)
router.register(r'items', ScrapedItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
