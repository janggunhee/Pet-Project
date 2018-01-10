import logging

import raven

from .base import *

# debug
DEBUG = True

# json filepath 설정
TEST_SECRET = os.path.join(CONFIG_SECRET_DIR, 'settings_test.json')
with open(TEST_SECRET, 'r') as settings_test:
    test_secret_common_str = settings_test.read()

test_secret_common = json.loads(test_secret_common_str)

# databases
DATABASES = test_secret_common['django']['databases']

# AWS
AWS_ACCESS_KEY_ID = test_secret_common['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = test_secret_common['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = test_secret_common['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = test_secret_common['aws']['s3-region-name']
AWS_S3_SIGNATURE_VERSION = test_secret_common['aws']['s3-signature-version']

# S3 FileStorage
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'

# AWS Storage
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


# AWS Healthchecker
private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)


# Installed Apps
INSTALLED_APPS += [
    'corsheaders',
    'raven.contrib.django.raven_compat',
]

# 프론트에서 요청이 들어올 때 장고가 허용해주는 도메인들
CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:8080',
    'localhost:4200',
    'wooltari-test-server-dev.ap-northeast-2.elasticbeanstalk.com',
    'wooltari.co.kr',
)

# MiddleWare CORS Settings
MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Raven Logging Settings
RAVEN_CONFIG = {
    'dsn': 'https://700ba3478d9944f385c16338e2c10976:15a82e91d9d64be9b099ae466f9d974f@sentry.io/256077',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(ROOT_DIR),
    'CELERY_LOGLEVEL': logging.INFO,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
