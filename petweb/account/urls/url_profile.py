from django.conf.urls import url

from .. import apis, views

urlpatterns = [
    # 유저 디테일 뷰 / 닉네임 수정 / 유저 삭제
    url(r'^(?P<user_pk>\d+)/', apis.UserDetailUpdateDestroy.as_view()),
]
