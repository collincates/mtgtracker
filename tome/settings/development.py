from .base import *


DEBUG = True

# Apps for Debug Toolbar
INSTALLED_APPS += ('debug_toolbar',)

# Middleware for Debug Toolbar
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# Connect to local PostgreSQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['PGDB_NAME'],
        'USER': os.environ['PGDB_USER'],
        'PASSWORD': os.environ['PGDB_PASS'],
        'HOST': os.environ['PGDB_HOST'],
        'PORT': os.environ['PGDB_PORT'],
    }
}

# Localhost
INTERNAL_IPS =['127.0.0.1']

# Console logging of email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
