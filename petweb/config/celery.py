import os

from celery import Celery

# celery가 초기 설정값을 config.settings에서 가져온다
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')

# celery가 config 폴더를 인식한다
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery가 config.settings에 인식된 모든 application의 tasks를 인식한다
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
