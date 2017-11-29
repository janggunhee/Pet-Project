from django.conf.urls import url
from django.contrib import admin

from account import views


urlpatterns = [
    url(r'^$', views.index, name='main'),
    url(r'^admin/', admin.site.urls, name='admin'),
]