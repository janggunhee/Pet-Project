from .base import *

# debug
DEBUG = True

# databases
# DATABASES = config_secret_common['django']['databases']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}