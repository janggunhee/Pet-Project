from django.conf.urls import url, include

urlpatterns = [
    url('^user/', include('account.urls.url_human', namespace='user')),
    url('^pet/', include('account.urls.url_pet', namespace='pet'))
]