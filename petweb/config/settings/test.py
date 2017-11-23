from .base import *

# debug
DEBUG = True

# databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': 'localhost',
        'NAME': 'pet',
        'USER': 'postgres'
    }
}

# email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
