from django.conf.urls import url

from . import apis

# 의료정보 관련
urlpatterns = [
    # 백신 정보 리스트
    url(r'vaccine-list/$', apis.VaccineInfoList.as_view(), name='vaccine-list'),
    # 동물이 맞은 백신 정보 리스트 / 생성
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/inoculations/$', apis.InoculationListCreate.as_view(),
        name='inoculation'),
    # 동물이 맞은 백신 정보 디테일 / 수정 / 삭제
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/inoculations/(?P<ino_pk>\d+)/$',
        apis.InoculationRetrieveUpdateDestroy.as_view(), name='inoculation-detail'),

    # 수술 정보 리스트 / 생성
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/operations/$', apis.OperationListCreate.as_view(), name='operation'),
    # 수술 정보 디테일 / 수정 / 삭제
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/operations/(?P<oper_pk>\d+)/$',
        apis.OperationRetrieveUpdateDestroy.as_view(), name='operation-detail'),

    # 신체 사이즈 리스트 / 생성
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/sizes', apis.BodySizeListCreate.as_view(), name='body-size'),
    # 신체 사이즈 디테일 / 수정 /삭제
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/sizes/(?P<body_pk>\d+)/', apis.BodySizeRetrieveUpdateDestroy.as_view(),
        name='body-size-detail'),

    # 의료 정보 디테일 뷰
    url(r'(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/$', apis.PetMedicalDetail.as_view(), name='detail')
]

# 지도 관련
urlpatterns += [
    # 주변 동물병원 검색
    url(r'search-hospital/$', apis.Hospital.as_view(), name='hospital'),
]
