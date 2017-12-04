from django.shortcuts import get_list_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import pagination, permissions
from ..models import Pet
from ..serializers import PetSerializer


__all__ = (
    'PetListCreate',
    'PetProfile',
)


# 펫 리스트 / 생성 뷰
class PetListCreate(generics.ListCreateAPIView):
    """
    펫의 리스트를 보고 펫을 생성하는 뷰

    1. 리스트 보기
        method: get

    2. 펫 생성
        method: post

    """
    # 쿼리셋: 반려동물 쿼리셋 전체
    queryset = Pet.objects.all()
    # 시리얼라이저: 펫 시리얼라이저
    serializer_class = PetSerializer
    # 페이지네이션: utils.pagination에 있는 pagination 사용
    pagination_class = pagination.StandardPetViewPagination
    # 권한: 소유주 이외에는 읽기만 가능
    permission_classes = (permissions.IsOwnerOrReadOnly, )
    # url 키워드 인자: user_pk
    lookup_url_kwarg = 'user_pk'

    # 데이터를 시리얼라이징해서 생성하는 메소드
    def perform_create(self, serializer):
        # 커스텀 세팅: owner 값을 현재 로그인한 유저로 설정한다
        serializer.save(owner=self.request.user)

    # 쿼리셋에서 객체를 가져오는 메소드
    def get_object(self):
        # 커스텀 세팅: 반려동물 쿼리셋을 가져올 때 필터링 옵션을 준다
        # 동물 주인의 pk값과 url에 들어온 user_pk 값이 일치하는 동물들만 가져오도록!
        filter_kwargs = {'owner_id': self.kwargs[self.lookup_url_kwarg]}
        # 필터링을 거친 쿼리셋을 리스트로 반환한다
        obj = get_list_or_404(self.get_queryset(), **filter_kwargs)

        # 리스트의 권한을 체크한다
        self.check_object_permissions(self.request, obj)

        return obj

    # 펫 리스트를 가져오는 뷰
    # method: get
    def get(self, request, *args, **kwargs):
        # 앞서 get_object 메소드로 가져온 instance 객체를 불러온다
        instance = self.get_object()

        # instance 객체를 페이지네이션 된 쿼리셋으로 변환한다
        page = self.paginate_queryset(instance)
        # 쿼리셋의 숫자가 많아서 page가 생성된다면
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 페이지네이션 응답을 리턴한다
            return self.get_paginated_response(serializer.data)

        # 만일 쿼리셋의 숫자가 적어서 page가 만들어지지 않는다면
        serializer = self.get_serializer(instance, many=True)
        # 일반 시리얼라이저 데이터를 리턴한다
        return Response(serializer.data)

    # 펫을 생성하는 뷰
    # method: post
    def post(self, request, *args, **kwargs):
        # 만일 post 요청을 보낸 user pk 값과 url에 담긴 user_pk 키워드 인자 값이 일치한다면
        # (자기 자신이 시도해야만 펫 생성이 가능하도록 설계한 것)
        if str(request.user.pk) == request.resolver_match.kwargs['user_pk']:
            # 위의 조건문을 만족하면 펫을 생성한다
            # mixins.CreateModelMixin의 create 함수를 그대로 가져옴
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # 만일 어떤 유저가 다른 유저의 user_pk값으로 펫을 생성하려고 시도한다면
        # 조건문을 만족하지 못해 에러 메시지를 출력한다
        error = {
            "detail": "You do not have permission to perform this action."
        }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)


# 펫 디테일 보기 뷰 (사람 나이 환산)
class PetProfile(APIView):
    def get(self, request, *args, **kwargs):
        pass