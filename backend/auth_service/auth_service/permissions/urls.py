from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermissionViewSet

router = DefaultRouter()
router.register('', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', PermissionViewSet.as_view({'get': 'categories'}), name='permission-categories'),
    path('by-category/', PermissionViewSet.as_view({'get': 'by_category'}), name='permissions-by-category'),
    path('my-permissions/', PermissionViewSet.as_view({'get': 'my_permissions'}), name='my-permissions'),
]
