from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.settings import api_settings

from medical.models import PetMedical
from utils.functions import pet_age
from utils.functions.making_thumb import making_thumbnail
from ..models import Pet, PetSpecies, PetBreed
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSpeciesField',
    'PetBreedField',
    'PetSerializer',
    'PetBreedSerializer',
)


# 펫 종류 관계 필드
class PetSpeciesField(serializers.RelatedField):
    queryset = PetSpecies.objects.all()

    class Meta:
        model = PetSpecies
        fields = ('pet_type',)

    # pk값 대신 'dog/cat'으로 보일 수 있도록 커스텀
    def to_representation(self, instance):
        return instance.pet_type

    # 입력 형식을 커스텀
    def to_internal_value(self, data):
        try:
            try:
                # dog/cat을 입력하면 거기에 맞는 인스턴스를 출력해준다
                return PetSpecies.objects.get(pet_type=data)
            # 예외 처리들
            except KeyError:
                raise serializers.ValidationError(
                    'data is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'data must be an "dog" or "cat".'
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'data does not exist.'
            )


# 펫 품종 관계 필드
class PetBreedField(serializers.RelatedField):
    queryset = PetBreed.objects.all()

    class Meta:
        model = PetBreed
        fields = ('breeds_name',)

    # pk값 대신 품종 이름이 보일 수 있도록 커스텀
    def to_representation(self, instance):
        return instance.breeds_name

    # 입력 형식을 커스텀
    def to_internal_value(self, data):
        try:
            try:
                # dog/cat을 입력하면 거기에 맞는 인스턴스를 출력해준다
                return PetBreed.objects.get(breeds_name=data)
            # 예외 처리들
            except KeyError:
                raise serializers.ValidationError(
                    'data is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'data must be an PetBreeds Objects.'
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'data does not exist.'
            )


# 펫의 내용을 보여주는 시리얼라이저
class PetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)  # 이름
    # http://www.django-rest-framework.org/api-guide/fields/#datefield
    birth_date = serializers.DateField(format=api_settings.DATE_FORMAT)  # 생년월일
    # RelatedField의 to_interval_value를 이용해 입력값을 제어
    # 참고: https://goo.gl/roNmog
    species = PetSpeciesField()  # 강아지/고양이
    breeds = PetBreedField()  # 품종
    # http://www.django-rest-framework.org/api-guide/fields/#choicefield
    gender = serializers.ChoiceField(choices=Pet.CHOICE_GENDER)  # 성별
    body_color = serializers.ChoiceField(choices=Pet.CHOICE_COLOR)  # 색상
    identified_number = serializers.CharField(max_length=20, allow_blank=True)  # 동물등록번호
    is_neutering = serializers.BooleanField(default=False)  # 중성화
    is_active = serializers.BooleanField(default=True)  # 활성화

    class Meta:
        model = Pet
        fields = (
            'pk',  # 동물pk
            'species',  # 강아지/고양이
            'breeds',  # 품종
            'name',  # 이름
            'birth_date',  # 생년월일
            'gender',  # 성별
            'body_color',  # 색깔
            'identified_number',  # 동물등록번호
            'is_neutering',  # 중성화
            'is_active',  # 활성화여부(동물사망/양도/입양)
            'image',
        )
        read_only_fields = (
            'pk',
        )

    # 펫 생성
    def create(self, validated_data):
        # 펫 생성
        created_pet = Pet.objects.create(**validated_data)
        # 펫 의료정보 생성
        PetMedical.objects.create(pet=created_pet)
        # 썸네일 생성
        thumbnail_pet = making_thumbnail(created_pet)
        # 썸네일 생성된 펫 리턴
        return thumbnail_pet

    # 출력 형식을 커스터마이징
    def to_representation(self, instance):
        # 생년월일을 토대로 반려동물의 나이를 계산하는 함수
        def calculate_pet_age(birth_date):
            # birth_date를 입력받아 나이를 리턴한다
            return pet_age.calculate_age(birth_date)

        # 반려동물이 사람으로 치면 몇 살인지를 계산하는 함수
        def human_age_conversion(instance):
            # 입력값에서 species와 breed 값을 가져와 각 모델에서 객체를 꺼낸다
            # 각 객체의 이름을 문자열로 꺼낸다
            str_pet_type = instance.species.pet_type
            str_pet_breed = instance.breeds
            birth_date = instance.birth_date
            conversed_age = pet_age.age_conversion(str_pet_type, str_pet_breed, birth_date)
            return conversed_age

        pet_birth_date = instance.birth_date
        result_pet_age = calculate_pet_age(pet_birth_date).years
        ages = {
            'pet_age': result_pet_age,
            'conversed_age': human_age_conversion(instance)
        }
        ret = super().to_representation(instance)
        data = {
            'owner': UserSerializer(instance.owner).data,
            'pet': ret,
            'ages': ages,
        }

        return data


# 사용자가 강아지/고양이를 선택하면 펫 품종을 보여주는 시리얼라이저
class PetBreedSerializer(serializers.ModelSerializer):
    species = PetSpeciesField(write_only=True)

    class Meta:
        model = PetBreed
        fields = (
            'species',
            'breeds_name',
        )
