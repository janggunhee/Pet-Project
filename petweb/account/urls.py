from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^login/$', apis.Login.as_view()),
    url(r'^signup/$', apis.Signup.as_view()),
    url(r'^detail/(?P<user_pk>\d+)/$', apis.UserDetail.as_view()),
]
