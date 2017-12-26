from django.conf.urls import url, include

from .. import apis

urlpatterns = [
    # 유저 디테일 뷰 / 정보 수정 / 유저 삭제
    url(r'^(?P<user_pk>\d+)/$', apis.UserProfileUpdateDestroy.as_view(), name='user'),
]

urlpatterns += [
    # 펫 품종 뷰
    url(r'^pet-breed-list/$', apis.PetBreedList.as_view(), name='pet-breed-list'),
    # 펫 리스트 / 펫 생성
    url(r'^(?P<user_pk>\d+)/pets/$', apis.PetListCreate.as_view(), name='pets'),
    # 펫 디테일 뷰
    url(r'^(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/$', apis.PetProfile.as_view(), name='pet-profile'),
    # 펫 나이 환산 뷰
    url(r'^(?P<user_pk>\d+)/pets/(?P<pet_pk>\d+)/age/$', apis.PetAge.as_view(), name='pet-age'),
]
