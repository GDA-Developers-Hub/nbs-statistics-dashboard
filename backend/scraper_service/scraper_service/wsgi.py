"""
WSGI config for SCRAPER microservice.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_service.settings')
application = get_wsgi_application()
