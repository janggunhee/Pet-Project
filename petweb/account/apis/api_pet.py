from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from utils.rest_framework import pagination, permissions
from utils.functions import pet_age
from ..models import Pet, PetSpecies, PetBreed
from ..serializers import *

User = get_user_model()

__all__ = (
    'PetListCreate',
    'PetAge',
    'PetProfile',
    'PetBreedList',
)


# 펫 리스트 / 생성 뷰
class PetListCreate(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = (permissions.IsUserOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        return Pet.objects.filter(owner_id=user)

    def perform_create(self, serializer):
        user = self.kwargs['user_pk']
        instance = User.objects.get(pk=user)
        self.check_object_permissions(self.request, instance)
        serializer.save(owner=instance)


# 펫 디테일 보기 뷰 / 정보 수정 / 펫 삭제
class PetProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    lookup_url_kwarg = 'pet_pk'

    def get_queryset(self):
        user = self.kwargs['user_pk']
        return Pet.objects.filter(owner_id=user)


# 펫 사람 나이 환산 뷰
class PetAge(generics.GenericAPIView):
    lookup_url_kwarg = 'pet_pk'

    def get_queryset(self):
        user = self.kwargs['user_pk']
        return Pet.objects.filter(owner_id=user)

    def get(self, request, *args, **kwargs):
        # 반려동물의 생년월일을 datetime 객체로 리턴하는 함수
        def pet_datetime_birth_date(serializer):
            # 입력값에서 birth_date를 가져온다
            raw_birth_date = serializer.data['pet']['birth_date']
            # 문자열 값인 raw_birth_date를 datetime 객체로 바꾼다
            datetime_birth_date = datetime.strptime(raw_birth_date, '%Y-%m-%d').date()
            return datetime_birth_date

        # 생년월일을 토대로 반려동물의 나이를 계산하는 함수
        def calculate_pet_age(birth_date):
            # birth_date를 입력받아 나이를 리턴한다
            return pet_age.calculate_age(birth_date)

        # 반려동물이 사람으로 치면 몇 살인지를 계산하는 함수
        def human_age_conversion(serializer):
            # 입력값에서 species와 breed 값을 가져와 각 모델에서 객체를 꺼낸다
            object_pet_type = PetSpecies.objects.get(pet_type=serializer.data['pet']['species'])
            object_pet_breed = PetBreed.objects.get(breeds_name=serializer.data['pet']['breeds'])
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


# 펫 품종 리스트 보기 뷰
class PetBreedList(generics.GenericAPIView):
    serializer_class = PetBreedSerializer

    def get_queryset(self):
        pet_type = self.request.data['species']
        return PetBreed.objects.filter(species__pet_type=pet_type)

    # method: post
    def post(self, request, *args, **kwargs):
        # 쿼리셋을 불러온다
        queryset = self.filter_queryset(self.get_queryset())
        # 만일 쿼리셋이 비어 있다면 (species 입력이 잘못되었을 경우)
        if len(queryset) == 0:
            # 에러 메시지를 보낸다
            error_message = {
                "detail": "Invalid or none value."
            }
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        # 이상 없다면 시리얼라이저를 만든다
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
