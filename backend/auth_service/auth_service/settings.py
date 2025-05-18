"""
Django settings for AUTH microservice.
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
SERVICE_NAME = 'auth_service'

# Override the base Django apps with service-specific apps
INSTALLED_APPS += [
    'auth_service.users',
    'auth_service.permissions',
    'auth_service.roles',
]

ROOT_URLCONF = 'auth_service.urls'
WSGI_APPLICATION = 'auth_service.wsgi.application'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# JWT-specific settings
SIMPLE_JWT.update({
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'JTI_CLAIM': 'jti',
})

# Custom authentication backend for RBAC
AUTHENTICATION_BACKENDS = [
    'auth_service.permissions.backends.RoleBasedPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Logging configuration
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'auth.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'security.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'auth_service': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
