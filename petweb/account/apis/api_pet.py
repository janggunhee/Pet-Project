from rest_framework import generics, status, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsOwnerOrReadOnly
from ..models import Pet
from ..serializers import UserSerializer, PetSerializer

__all__ = (
    'PetListCreate',
)


"""
generics.ListCreateAPIView
1. 로그인한 상태에서 내 펫의 목록을 보는 뷰 (get)
    1. 시리얼라이저 페이지네이션 필요
    2. 커스텀 필터링
2. 내 펫을 생성하는 뷰 (post)
    1. 생성용 시리얼라이저 필요

generics.RetrieveUpdateDestroyAPIView
3. 하나의 펫을 디테일하게 보는 뷰 (get)
4. 펫의 내용을 수정하는 뷰 (patch)
    1. 수정용 시리얼라이저 필요
5. 펫을 삭제하는 뷰 (delete)

"""


class PetListCreate(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_url_kwarg = 'user_pk'

    def get_queryset(self):
        queryset = Pet.objects.filter(owner_id=self.request.user.pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
