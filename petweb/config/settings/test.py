from .base import *

# debug
DEBUG = True

# databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'pet',
        'USER': 'lanark'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
