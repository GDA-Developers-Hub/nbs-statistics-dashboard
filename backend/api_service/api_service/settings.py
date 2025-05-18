"""
Django settings for API microservice.
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
SERVICE_NAME = 'api_service'

# Override the base Django apps with service-specific apps
INSTALLED_APPS += [
    'api_service.regions',
    'api_service.sectors',
    'api_service.indicators',
    'api_service.statistics',
]

ROOT_URLCONF = 'api_service.urls'
WSGI_APPLICATION = 'api_service.wsgi.application'

# Define cache settings for API service
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', '6379')}",
        'OPTIONS': {
            'db': '1',
            'parser_class': 'redis.connection.PythonParser',
            'pool_class': 'redis.BlockingConnectionPool',
        }
    }
}

# Cache timeouts in seconds for different endpoints
CACHE_TTL = {
    'regions': 60 * 60 * 24,  # 24 hours for regions list
    'sectors': 60 * 60 * 24,  # 24 hours for sectors list
    'indicators': 60 * 10,    # 10 minutes for indicators
    'key_stats': 60 * 5,      # 5 minutes for key stats
    'summary': 60 * 15,       # 15 minutes for summary stats
}
