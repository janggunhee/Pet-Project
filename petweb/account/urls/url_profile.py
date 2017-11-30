from django.conf.urls import url, include

from . import url_pet
from .. import apis

urlpatterns = [
    # 유저 디테일 뷰 / 닉네임 수정 / 유저 삭제
    url(r'^(?P<user_pk>\d+)/$', apis.UserProfileUpdateDestroy.as_view(), name='user'),
    url(r'^(?P<user_pk>\d+)/', include(url_pet, namespace='pet')),
]
