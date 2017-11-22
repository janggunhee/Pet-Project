from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^signup/$', views.Signup.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', views.UserDetail.as_view()),
]
