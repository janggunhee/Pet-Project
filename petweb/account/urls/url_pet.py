from django.conf.urls import url

from .. import apis

urlpatterns = [
    url('^list/$', apis.PetListCreate.as_view(), name='pet-list')
]