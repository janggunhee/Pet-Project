from .base import *

# Allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# debug
DEBUG = True

# databases
DATABASES = config_secret_common['django']['databases']
