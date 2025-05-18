from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jobs', views.ScraperJobViewSet, basename='scraperjob')
router.register(r'scraped-items', views.ScrapedItemViewSet, basename='scrapeditem')

urlpatterns = [
    path('', include(router.urls)),
    path('latest-statistics/', views.latest_statistics, name='latest-statistics'),
    
    # Real-time scraping endpoints
    path('realtime/trigger/', views.trigger_realtime_scrape, name='trigger-realtime-scrape'),
    path('realtime/data/', views.realtime_data, name='realtime-data'),
    path('realtime/data/<str:category>/', views.realtime_data, name='realtime-data-category'),
]
