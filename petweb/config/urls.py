"""petweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from account import views

# 메인 화면 및 관리자 페이지
urlpatterns = [
    # 메인 페이지
    url(r'^$', views.index, name='main'),
    # 어드민 페이지
    url(r'^admin/', admin.site.urls, name='admin'),
]

# 나머지 페이지의 시작 분기점
urlpatterns += [
    # 회원 관리 url → account.urls.url_auth로 연결됨
    # 회원가입, 로그인, 페이스북 로그인 기능 수행
    url(r'auth/', include('account.urls.url_auth', namespace='auth')),
    # 회원 프로필 url → account.urls.url_profile로 연결됨
    # 회원 프로필, 정보(닉네임/비밀번호) 수정, 회원 삭제 기능 수행
    url(r'profile/', include('account.urls.url_profile', namespace='profile')),
]

# media
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
