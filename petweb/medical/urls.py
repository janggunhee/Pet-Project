from django.conf.urls import url

from . import views

# 의료정보 관련
urlpatterns = [

]

# 지도 관련
urlpatterns += [
    url(r'search-hospital/', views.Hospital.as_view(), name='hospital'),
]
