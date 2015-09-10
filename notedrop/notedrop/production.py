from notedrop.settings import *


ALLOWED_HOSTS = ['*',]

ADMINS = (
    ('Nathan Papes', 'papes1ns@cmich.edu'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'notedrop',
        'USER': 'notedrop',
        'PASSWORD': 'aFD0#$y`(^Ho|}?T.N'vp9*'0dM?[t`*cm?U@d[wM+:P/ZK].:pM)|\\gp~k(ZV',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}
