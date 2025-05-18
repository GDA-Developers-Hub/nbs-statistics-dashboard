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
    'django_crontab',  # Add the crontab app
]

ROOT_URLCONF = 'scraper_service.urls'
WSGI_APPLICATION = 'scraper_service.wsgi.application'

# Crontab settings (schedule tasks)
CRONJOBS = [
    # Run the Somalia scraper every 20 minutes
    ('*/20 * * * *', 'django.core.management.call_command', ['run_somalia_scraper_test']),
]

# Scraper settings
SCRAPER_CONFIG = {
    'base_url': 'https://nbs.gov.so/',
    'user_agent': 'SNBS Dashboard Scraper/1.0',
    'request_timeout': 30,
    'request_delay': 1.0,
    'max_retries': 3,
    
    # Paths to scrape
    'statistics_path': '/statistics',
    'publications_path': '/publications',
    
    # PDF settings
    'pdf_max_pages': 50,
    'pdf_tables_per_page': 3,
    
    # Schedule intervals (in hours or minutes, e.g. '24h', '30m')
    'schedule_interval': {
        'somalia_stats': '20m',  # Every 20 minutes for real-time updates
        'publications': '6h',    # Every 6 hours for publications
    },
    
    # Real-time scraping settings
    'real_time_categories': ['demographics', 'economy', 'inflation'],  # Categories to prioritize for real-time updates
    'enable_websocket_updates': True,  # Enable WebSocket notifications for new data
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
    'statistics': int(os.environ.get('SCRAPER_SCHEDULE_INTERVAL', '20')),  # minutes (default: 20 minutes)
    'publications': int(os.environ.get('SCRAPER_SCHEDULE_INTERVAL', '1440')) * 7,  # minutes (default: weekly)
}

# Add schedule package for scheduled jobs
try:
    import schedule
except ImportError:
    raise ImportError("Required package 'schedule' is not installed. Run 'pip install schedule'.")

# Try to import pandas and bs4 for scraping
try:
    import pandas as pd
    import bs4
except ImportError:
    raise ImportError("Required packages for scraping are not installed. Run 'pip install pandas beautifulsoup4 lxml html5lib tabula-py'.")
