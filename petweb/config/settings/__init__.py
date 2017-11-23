import os
from ..celery import app as celery_app

# celery.py의 app 변수를 celery_app으로 이름붙이고
# settings.__init__에 추가한다
__all__ = ['celery_app']

# 세팅 모듈의 기본값은 로컬을 사용한다
SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings':
    from .local import *
