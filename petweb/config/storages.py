from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    # AWS S3는 절대경로를 지원하지 않는다. 따라서 이미지 url을 꺼내려고 할 경우 'NotImplementedError'가 발생한다
    # 해결책은 이 사이트를 참고했다: http://blog.hardlycode.com/solving-django-storage-notimplementederror-2011-01/
    # 공식 문서: https://docs.djangoproject.com/en/1.11/ref/files/storage/#django.core.files.storage.Storage.path
    def path(self, name):
        return None
