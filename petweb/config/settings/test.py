from .base import *

# debug
DEBUG = True

# databases
DATABASES = config_secret_common['django']['databases']

# databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'NAME': 'pet',
#         'USER': 'postgres'
#     }
# }

# email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
