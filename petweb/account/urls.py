from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^signup/$', views.Signup.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', views.Delete.as_view()),
]
