from django.conf.urls import url

from . import apis

# 의료정보 관련
urlpatterns = [
    # 백신 정보 리스트
    url(r'vaccine-list/$', apis.VaccineInfoList.as_view(), name='vaccine-list'),
    # 동물이 맞은 백신 정보 리스트 / 생성
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/inoculations/$', apis.PetVaccineInoculation.as_view(), name='vaccine'),
    # 동물이 맞은 백신 정보 수정 / 삭제
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/inoculations/(?P<ino_pk>\d+)/$',
        apis.PetVaccineInoculationUpdateDestroy.as_view(), name='vaccine-detail'),
    # 수술 정보 리스트 / 생성 뷰
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/operations/$', apis.PetOperation.as_view(), name='operation'),
    # 신체 사이즈 리스트 / 생성 뷰
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/sizes', apis.PetSize.as_view(), name='pet-size'),
    # 의료 정보 디테일 뷰
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/$', apis.PetMedicalDetail.as_view(), name='detail')
]

# 지도 관련
urlpatterns += [
    # 주변 동물병원 검색
    url(r'search-hospital/$', apis.Hospital.as_view(), name='hospital'),
]
