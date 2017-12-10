from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from utils import pagination, pet_age, \
    permissions as custom_permissions
from ..models import Pet, PetSpecies, PetBreed
from ..serializers import PetSerializer, PetCreateSerializer, UserSerializer

User = get_user_model()

__all__ = (
    'PetListCreate',
    'PetAge',
    'PetProfile',
)


# 펫 리스트 / 생성 뷰
class PetListCreate(generics.GenericAPIView):
    """
    펫의 리스트를 보고 펫을 생성하는 뷰

    1. 리스트 보기
        method: get

    2. 펫 생성
        method: post

    """
    # # 쿼리셋: 반려동물 쿼리셋 전체
    # queryset = Pet.objects.all()
    # # 시리얼라이저: 펫 시리얼라이저
    # serializer_class = PetSerializer
    # 페이지네이션: utils.pagination에 있는 pagination 사용
    pagination_class = pagination.StandardPetViewPagination
    # 권한: 소유주 이외에는 읽기만 가능
    permission_classes = (custom_permissions.IsOwnerOrReadOnly, )
    # url 키워드 인자: user_pk
    lookup_url_kwarg = 'user_pk'

    # 데이터를 시리얼라이징해서 생성하는 메소드
    def perform_create(self, serializer):
        # AbstractBaseUser가 is_active=False 로 설정되어 있어서
        # Pet도 이 설정을 그대로 상속받는 이슈가 있었다
        # PetCreateSerializer에서 default=True로 설정하는 것으로 변경
        serializer.save(owner=self.request.user)

    # 쿼리셋에서 객체를 가져오는 메소드
    def get_object(self):
        # 커스텀 세팅: 반려동물 쿼리셋을 가져올 때 필터링 옵션을 준다
        # 동물 주인의 pk값과 url에 들어온 user_pk 값이 일치하는 동물들만 가져오도록!
        filter_kwargs = {'id': self.kwargs[self.lookup_url_kwarg]}
        # 필터링을 거친 쿼리셋을 리스트로 반환한다
        obj = get_object_or_404(self.get_queryset(), **filter_kwargs)

        # 리스트의 권한을 체크한다
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        if self.request.method in permissions.SAFE_METHODS:
            return User.objects.all()
        return Pet.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializer
        return PetCreateSerializer

    # 펫 리스트를 가져오는 뷰
    # method: get
    def get(self, request, *args, **kwargs):
        # 앞서 get_object 메소드로 가져온 instance 객체를 불러온다
        instance = self.get_object()

        # # instance 객체를 페이지네이션 된 쿼리셋으로 변환한다
        # page = self.paginate_queryset(instance)
        # # 쿼리셋의 숫자가 많아서 page가 생성된다면
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     # 페이지네이션 응답을 리턴한다
        #     return self.get_paginated_response(serializer.data)

        # 만일 쿼리셋의 숫자가 적어서 page가 만들어지지 않는다면
        user_serializer = self.get_serializer(instance)
        data = {
            'owner': user_serializer.data,
            'pets': PetSerializer(instance.pets, many=True, context={'request': request}).data
        }

        # 일반 시리얼라이저 데이터를 리턴한다
        return Response(data, status=status.HTTP_200_OK)

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 만일 어떤 유저가 다른 유저의 user_pk값으로 펫을 생성하려고 시도한다면
        # 조건문을 만족하지 못해 에러 메시지를 출력한다
        error = {
            "detail": "You do not have permission to perform this action."
        }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)


# 펫 사람 나이 환산 뷰
class PetAge(generics.GenericAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = (custom_permissions.IsOwnerOrReadOnly, )
    lookup_field = ('owner_id', 'pk')
    lookup_url_kwarg = ('user_pk', 'pet_pk')

    # 쿼리셋에서 객체를 가져오는 메소드
    def get_object(self):
        # 커스텀 세팅: 반려동물 쿼리셋을 가져올 때 필터링 옵션을 준다
        # 동물 주인의 pk값과 url에 들어온 user_pk 값이 일치하는 동물들만 가져오도록!
        # 쿼리셋: 위에서 정의한 펫 쿼리셋
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            key: self.kwargs[value]
            # lookup_field와 lookup_url_kwarg를 동시에 순회하면서
            # key에는 lookup_field의 값을,
            # value에는 전체 키워드 인자 묶음 중 lookup_url_kwarg를 key로 하는 값을 넣는다
            for key, value in zip(self.lookup_field, self.lookup_url_kwarg)
        }

        # 쿼리셋과 키워드 인자 묶음으로 펫 인스턴스를 받는다
        obj = get_object_or_404(queryset, **filter_kwargs)
        # 인스턴스의 권한을 체크한다
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request, *args, **kwargs):
        # 반려동물의 생년월일을 datetime 객체로 리턴하는 함수
        def pet_datetime_birth_date(serializer):
            # 입력값에서 birth_date를 가져온다
            raw_birth_date = serializer.data['birth_date']
            # 문자열 값인 raw_birth_date를 datetime 객체로 바꾼다
            datetime_birth_date = datetime.strptime(raw_birth_date, '%Y-%M-%d').date()
            return datetime_birth_date

        # 생년월일을 토대로 반려동물의 나이를 계산하는 함수
        def calculate_pet_age(birth_date):
            # birth_date를 입력받아 나이를 리턴한다
            return pet_age.calculate_age(birth_date)

        # 반려동물이 사람으로 치면 몇 살인지를 계산하는 함수
        def human_age_conversion(serializer):
            # 입력값에서 species와 breed 값을 가져와 각 모델에서 객체를 꺼낸다
            object_pet_type = PetSpecies.objects.get(pet_type=serializer.data['species'])
            object_pet_breed = PetBreed.objects.get(breeds_name=serializer.data['breeds'])
            # 각 객체의 이름을 문자열로 꺼낸다
            str_pet_type = object_pet_type.pet_type
            str_pet_breed = object_pet_breed.breeds_name
            birth_date = pet_datetime_birth_date(serializer)
            conversed_age = pet_age.age_conversion(str_pet_type, str_pet_breed, birth_date)
            return conversed_age

        # user_pk에 맞는 펫 쿼리셋 호출
        instance = self.get_object()
        # 이상 없으면 펫 객체 디테일을 생성
        # PetSerializer가 HyperlinkedidentifyField를 갖게 되어서
        # 시리얼라이저에 request를 전달해준다
        serializer = PetSerializer(instance, context={'request': request})
        # 펫의 생년월일
        pet_birth_date = pet_datetime_birth_date(serializer)
        # 펫의 나이에서 개월 수 제외하고 년도만 출력
        result_pet_age = calculate_pet_age(pet_birth_date).years

        # 최종 출력 데이터: 펫의 나이와 사람 나이 환산 값
        data = {
            'pet_age': result_pet_age,
            'conversed_age': human_age_conversion(serializer)
        }

        return Response(data, status=status.HTTP_200_OK)


# 펫 디테일 보기 뷰 / 정보 수정 / 펫 삭제
class PetProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = (custom_permissions.IsOwnerOrReadOnly, )
    lookup_field = ('owner_id', 'pk')
    lookup_url_kwarg = ('user_pk', 'pet_pk')

    # 쿼리셋에서 객체를 가져오는 메소드
    def get_object(self):
        # 커스텀 세팅: 반려동물 쿼리셋을 가져올 때 필터링 옵션을 준다
        # 동물 주인의 pk값과 url에 들어온 user_pk 값이 일치하는 동물들만 가져오도록!
        # 쿼리셋: 위에서 정의한 펫 쿼리셋
        queryset = self.filter_queryset(self.get_queryset())
        # 딕셔너리 컴프리헨션
        filter_kwargs = {
            key: self.kwargs[value]
            # lookup_field와 lookup_url_kwarg를 동시에 순회하면서
            # key에는 lookup_field의 값을,
            # value에는 전체 키워드 인자 묶음 중 lookup_url_kwarg를 key로 하는 값을 넣는다
            for key, value in zip(self.lookup_field, self.lookup_url_kwarg)
        }

        # 쿼리셋과 키워드 인자 묶음으로 펫 인스턴스를 받는다
        obj = get_object_or_404(queryset, **filter_kwargs)
        # 인스턴스의 권한을 체크한다
        self.check_object_permissions(self.request, obj)

        return obj

    # 펫 디테일 보기 뷰
    # method: get
    def retrieve(self, request, *args, **kwargs):
        # RetrieveModelMixin을 상속
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 출력 형식을 일정하게 만들기 위해 커스텀
        data = {
            'owner': UserSerializer(instance.owner).data,
            'pet': serializer.data
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        # UpdateModelMixin을 상속
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # 출력 형식을 일정하게 만들기 위해 커스텀
        data = {
            'owner': UserSerializer(instance.owner).data,
            'pet': serializer.data
        }
        return Response(data)
