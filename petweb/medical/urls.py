from django.conf.urls import url

from . import apis

# 의료정보 관련
urlpatterns = [
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/$', apis.PetVaccineInoculation.as_view(), name='vaccine'),

]

# 지도 관련
urlpatterns += [
    url(r'search-hospital/', apis.Hospital.as_view(), name='hospital'),
]
