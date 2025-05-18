from django.urls import path
from .views import StatisticsViewSet

urlpatterns = [
    path('summary/', StatisticsViewSet.as_view({'get': 'summary'}), name='statistics-summary'),
    path('recent-updates/', StatisticsViewSet.as_view({'get': 'recent_updates'}), name='statistics-recent-updates'),
    path('dashboard/', StatisticsViewSet.as_view({'get': 'dashboard_data'}), name='statistics-dashboard'),
]
