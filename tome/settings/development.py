from .base import *


DEBUG = True

# Apps for Debug Toolbar
INSTALLED_APPS += ('debug_toolbar',)

# Middleware for Debug Toolbar
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# Localhost
INTERNAL_IPS =['127.0.0.1']

# Console logging of email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
