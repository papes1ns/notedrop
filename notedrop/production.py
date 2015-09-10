from notedrop.settings import *


ALLOWED_HOSTS = ['*',]

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

STATIC_ROOT = '/webapps/notedrop_env/notedrop/static/'
