from django.conf.urls import url

from . import apis, views

urlpatterns = [
    # 유저 로그인
    url(r'^login/$', apis.Login.as_view(), name='login'),
    # 프론트 페이스북 로그인
    url(r'^front-facebook-login/$', views.FrontFacebookLogin.as_view(), name='front-facebook-login'),
    # 페이스북 로그인
    url(r'^facebook-login/$', apis.FacebookLogin.as_view(), name='api-facebook-login'),
    # 유저 회원가입
    url(r'^signup/$', apis.Signup.as_view(), name='signup'),
    # 유저 디테일 뷰 / 닉네임 수정 / 유저 삭제
    url(r'^detail/(?P<user_pk>\d+)/$', apis.UserDetailUpdateDestroy.as_view()),
    # 유저 회원가입 후 이메일 활성화 뷰
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/$', apis.Activate.as_view(), name='activate'),
]
