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
from django.conf.urls import url, include
from django.contrib import admin

from account import views


# 메인 화면 및 관리자 페이지
urlpatterns = [
    url(r'^$', views.index, name='main'),
    url(r'^admin/', admin.site.urls, name='admin'),
]

# 나머지 페이지의 시작 분기점
urlpatterns += [
    # 회원 관리 url
    url(r'auth/', include('account.urls.url_auth', namespace='auth')),
    # 회원 프로필 url
    url(r'profile/', include('account.urls.url_profile', namespace='profile')),
]

