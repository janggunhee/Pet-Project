from .base import *

# Allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# databases
DATABASES = config_secret_common['django']['databases']
