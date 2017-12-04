from django.conf.urls import url

from .. import apis, views

urlpatterns = [
    # 유저 회원가입
    url(r'^signup/$', apis.Signup.as_view(), name='signup'),
    # 유저 회원가입 후 이메일 활성화 뷰
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/$', apis.Activate.as_view(), name='activate'),
    # 유저 로그인
    url(r'^login/$', apis.Login.as_view(), name='login'),
    # 프론트 페이스북 로그인
    url(r'^front-facebook-login/$', views.FrontFacebookLogin.as_view(), name='front-facebook-login'),
    # 페이스북 로그인
    url(r'^facebook-login/$', apis.FacebookLogin.as_view(), name='api-facebook-login'),
    # 유저 로그아웃
    url(r'^logout/$', apis.Logout.as_view(), name='logout'),

]