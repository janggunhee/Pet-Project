# 썸네일 생성 함수
import mimetypes
import os
from PIL import Image
from django.core.files.storage import default_storage


def making_thumbnail(instance):
    # 참고 1: PIL로 이미지 썸네일로 만들고 파일명 바꿔 저장하기 (StackOverFlow: https://goo.gl/d9G7V5)
    # 참고 2: PIL 이미지를 S3 bucket에 저장하기 (StackOverFlow: https://goo.gl/VAmyLZ)
    if ('_thumb' or 'placeholder') in instance.image.name:
        return instance
    raw_image = default_storage.open(instance.image.name, 'rb')
    img = Image.open(raw_image)
    img.thumbnail((300, 300), Image.ANTIALIAS)

    image_filename, image_extension = os.path.splitext(raw_image.name)
    image_extension = image_extension.lower()

    thumb_filename = image_filename + '_thumb' + image_extension

    mime = mimetypes.guess_type(thumb_filename)[0]
    file_type = mime.split('/')[1]

    img.save(thumb_filename, file_type)

    ret = thumb_filename.split('/.media/')

    instance.image = ret[1]

    return instance
