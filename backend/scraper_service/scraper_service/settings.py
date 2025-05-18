"""
Django settings for SCRAPER microservice.
Extends the core settings.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR.parent))

# Import core settings
from core.settings import *

# Service-specific settings
SERVICE_NAME = 'scraper_service'

# Override the base Django apps with service-specific apps
INSTALLED_APPS += [
    'scraper_service.scraper',
]

ROOT_URLCONF = 'scraper_service.urls'
WSGI_APPLICATION = 'scraper_service.wsgi.application'

# Scraper-specific settings
SCRAPER_CONFIG = {
    'base_url': os.environ.get('SNBS_BASE_URL', 'https://nbs.gov.so/'),
    'user_agent': 'SNBS Dashboard/1.0 (Data Collection Bot)',
    'request_timeout': 30,  # seconds
    'request_delay': 2,  # seconds between requests
    'max_retries': 3,  # maximum number of retries for failed requests
    
    # Paths to scrape
    'statistics_path': 'Statistics/',
    'publications_path': 'Publications/',
    
    # PDF processing settings
    'pdf_max_pages': 50,  # maximum number of pages to process per PDF
    'pdf_tables_per_page': 5,  # maximum number of tables to extract per page
}

# RabbitMQ settings for message publishing
RABBITMQ = {
    'host': os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
    'port': int(os.environ.get('RABBITMQ_PORT', '5672')),
    'user': os.environ.get('RABBITMQ_USER', 'guest'),
    'password': os.environ.get('RABBITMQ_PASSWORD', 'guest'),
    'vhost': os.environ.get('RABBITMQ_VHOST', '/'),
    'exchange': 'snbs_data_exchange',
    'statistics_queue': 'statistics_data',
    'publications_queue': 'publications_data',
}

# Schedule settings for different scraper types
SCRAPER_SCHEDULE = {
    'statistics': int(os.environ.get('SCRAPER_SCHEDULE_INTERVAL', '1440')),  # minutes (default: daily)
    'publications': int(os.environ.get('SCRAPER_SCHEDULE_INTERVAL', '1440')) * 7,  # minutes (default: weekly)
}
