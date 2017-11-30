from django.conf.urls import url

from .. import apis

urlpatterns = [
    url('^pets/', apis.PetListCreate.as_view(), name='pet-list')
]