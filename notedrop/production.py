from notedrop.settings import *


ALLOWED_HOSTS = ['52.88.79.68',]

ADMINS = (
    ('Nathan Papes', 'papes1ns@cmich.edu'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ubuntu',
        'USER': 'ubuntu',
        'PASSWORD': 'ubuntu',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

STATIC_ROOT = '/opt/notedrop/static/'
MEDIA_ROOT = '/opt/notedrop/media/'
