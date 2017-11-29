from django.conf.urls import url, include

from . import account, index

urlpatterns = [
    url(r'', include(index, namespace='index')),
    url(r'^account/', include(account, namespace='account')),
]
