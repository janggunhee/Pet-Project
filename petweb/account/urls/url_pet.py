from django.conf.urls import url

from .. import apis

urlpatterns = [
    url('^pet/$', apis.PetList.as_view(), name='pet-list')
]