from django.conf.urls import url

from . import apis

urlpatterns = [
    # 유저 로그인
    url(r'^login/$', apis.Login.as_view()),
    # 유저 회원가입
    url(r'^signup/$', apis.Signup.as_view()),
    # 유저 디테일 뷰 / 닉네임 수정 / 유저 삭제
    url(r'^detail/(?P<user_pk>\d+)/$', apis.UserDetail.as_view()),
    # 유저 회원가입 후 이메일 활성화 뷰
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9a-z]+)/$', apis.Activate.as_view(), name='activate'),
]
