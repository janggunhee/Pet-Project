import os

# 세팅 모듈의 기본값은 로컬을 사용한다
SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings':
    from .local import *
