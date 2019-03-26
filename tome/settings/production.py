from .base import *
import django_heroku
import dj_database_url


DEBUG = False

ALLOWED_HOSTS = ['https://mtgtome.herokuapp.com/']

# Add Whitenoise static file management
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Connect to remote PostgreSQL database using Heroku config variable DATABASE_URL
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Point collected static files to Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())
