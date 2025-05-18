from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegionAccessViewSet, UserSectorAccessViewSet

router = DefaultRouter()
router.register('', UserViewSet)
router.register('region-access', UserRegionAccessViewSet)
router.register('sector-access', UserSectorAccessViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('profile/', UserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='user-profile'),
]
