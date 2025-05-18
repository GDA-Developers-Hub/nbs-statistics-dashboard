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
})

# Custom authentication backend for RBAC
AUTHENTICATION_BACKENDS = [
    'auth_service.permissions.backends.RoleBasedPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]
