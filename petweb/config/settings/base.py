"""
Django settings for petweb project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os

# pet_project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

# pet_project/.config_secret
CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
COMMON_SECRET = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')

with open(COMMON_SECRET, 'r') as settings_common:
    config_secret_common_str = settings_common.read()

config_secret_common = json.loads(config_secret_common_str)

# Static paths
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')

# Media paths
MEDIA_URL = '/media/'
MEDIA_DIR = os.path.join(ROOT_DIR, '.media')

# Template paths
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Allowed hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.elasticbeanstalk.com',
    '.wooltari.co.kr',
]

# auth
# auth_user_model 정의
AUTH_USER_MODEL = 'account.User'

# facebook authentication 추가
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.backends.FacebookBackend',
]

# auth_password_validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# email
EMAIL_SECRET = os.path.join(CONFIG_SECRET_DIR, 'settings_email.json')
with open(EMAIL_SECRET, 'r') as settings_email:
    config_secret_email_str = settings_email.read()

config_secret_email = json.loads(config_secret_email_str)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
# 지메일 서버 사용
EMAIL_HOST = 'smtp.gmail.com'
# 보내는 사람 아이디/비밀번호 (secret 정보로 빼야 한다)
EMAIL_HOST_USER = config_secret_email['gmail']['username']
EMAIL_HOST_PASSWORD = config_secret_email['gmail']['password']
# 통신 포트
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Facebook
# app_id (공개 키)
FACEBOOK_APP_ID = config_secret_common['facebook']['app_id']
# secret_code (암호화 키)
FACEBOOK_APP_SECRET_CODE = config_secret_common['facebook']['secret_code']
# 요청할 개인정보 범위
# 참고: https://developers.facebook.com/docs/facebook-login/overview
# 로그인 검수 : 검수 절차를 받지 않은 앱에서 사용자에게 요청할 수 있는 권한은 다음과 같습니다.
FACEBOOK_SCOPE = [
    'public_profile',
    'email',
    'user_friends',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party app
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    # User app
    'account',
]


# rest_framework settings
REST_FRAMEWORK = {
    # test할 때 default 포맷을 json으로 세팅한다
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # TokenAuthentication
        'rest_framework.authentication.TokenAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# wsgi configuration
WSGI_APPLICATION = 'config.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Secret_key
SECRET_KEY = config_secret_common['django']['secret_key']


# AWS elasticbeanstalk HealthCheck
def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None
