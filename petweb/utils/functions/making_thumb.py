# 썸네일 생성 함수
import mimetypes
import os
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO


def making_thumbnail(instance):
    # 참고 1: PIL로 이미지 썸네일로 만들고 파일명 바꿔 저장하기 (StackOverFlow: https://goo.gl/d9G7V5)
    # 참고 2: PIL 이미지를 S3 bucket에 저장하기 (StackOverFlow: https://goo.gl/VAmyLZ)

    # 예외처리: 이미 썸네일 파일이거나 디폴트 이미지가 지정된 경우 프로세스를 건너뛴다
    if '_thumb' or 'placeholder' in instance.image.name:
        return instance

    # 원본 이미지를 인스턴스로부터 불러오기
    raw_image = default_storage.open(instance.image.name, 'rb')
    img = Image.open(raw_image)
    img.thumbnail((300, 300), Image.ANTIALIAS)

    # 썸네일 파일명 가공
    image_filename, image_extension = os.path.splitext(raw_image.name)
    image_extension = image_extension.lower()
    thumb_filename = image_filename + '_thumb' + image_extension
    split_filename = thumb_filename.split('/.media/')[1]

    # 파일 타입 생성
    mime = mimetypes.guess_type(thumb_filename)[0]
    file_type = mime.split('/')[1]

    # 파일 객체 저장
    temp_thumb = BytesIO()
    img.save(temp_thumb, file_type)
    temp_thumb.seek(0)

    # 파일 객체를 인스턴스에 저장
    instance.image.save(split_filename, ContentFile(temp_thumb.read()), save=True)
    temp_thumb.close()

    return instance
