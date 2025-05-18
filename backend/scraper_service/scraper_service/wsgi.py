"""
WSGI config for scraper_service project.
"""

import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_service.settings')

# Get the WSGI application
application = get_wsgi_application()

# Start the scraper scheduler
try:
    from scraper_service.scheduler import scheduler
    scheduler.start()
    logger.info("Started scraper scheduler")
except Exception as e:
    logger.exception(f"Failed to start scraper scheduler: {str(e)}")
