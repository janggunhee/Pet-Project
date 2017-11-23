from .base import *

# debug
DEBUG = True

# databases
DATABASES = config_secret_common['django']['databases']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'