from .celery import app as celery_app

# celery.py의 app 변수를 celery_app으로 이름붙이고
# settings.__init__에 추가한다
__all__ = ['celery_app']
