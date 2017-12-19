from django.conf.urls import url

from . import apis

# 의료정보 관련
urlpatterns = [

]

# 지도 관련
urlpatterns += [
    url(r'search-hospital/', apis.Hospital.as_view(), name='hospital'),
]
