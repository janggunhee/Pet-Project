from django.conf.urls import url

from . import apis

# 의료정보 관련
urlpatterns = [
    # 동물이 맞은 백신 정보 리스트 / 생성
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/vaccines/$', apis.PetVaccineInoculation.as_view(), name='vaccine'),

]

# 지도 관련
urlpatterns += [
    # 주변 동물병원 검색
    url(r'search-hospital/$', apis.Hospital.as_view(), name='hospital'),
]
