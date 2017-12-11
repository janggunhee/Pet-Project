from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.settings import api_settings

from ..relations import MultiplePKsHyperlinkedIdentityField
from ..models import Pet, PetSpecies, PetBreed
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSpeciesSerializer',
    'PetBreedSerializer',
    'PetSerializer',
    'PetCreateSerializer',
)


# 펫 종류 시리얼라이저
class PetSpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetSpecies
        fields = ('pet_type', )

    # pk값 대신 'dog/cat'으로 보일 수 있도록 커스텀
    def to_representation(self, instance):
        return instance.get_pet_type_display()


# 펫 품종 시리얼라이저
class PetBreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetBreed
        fields = ('breeds_name', )

    # pk값 대신 품종 이름이 보일 수 있도록 커스텀
    def to_representation(self, instance):
        return instance.breeds_name


# 펫의 내용을 보여주는 시리얼라이저
class PetSerializer(serializers.ModelSerializer):
    # 펫 종류는 PetSpeciesSerializer로 가공된다
    species = PetSpeciesSerializer()
    # 펫 품종은 PetBreedSerializer로 가공된다
    breeds = PetBreedSerializer()
    # 펫 나이는 PetAge 뷰를 URL 값으로 보여주도록 설계
    # 여러 개의 키워드 인자 값을 받기 위해 필드를 커스텀
    ages = MultiplePKsHyperlinkedIdentityField(
        view_name='profile:pet-age',
        lookup_fields=['owner_id', 'pk'],
        lookup_url_kwargs=['user_pk', 'pet_pk']
    )

    class Meta:
        model = Pet
        fields = (
            'pk',    # 동물pk
            'species',  # 강아지/고양이
            'breeds',  # 품종
            'name',  # 이름
            'birth_date',  # 생년월일
            'gender',  # 성별
            'body_color',  # 색깔
            'identified_number',  # 동물등록번호
            'is_neutering',  # 중성화
            'is_active',  # 활성화여부(동물사망/양도/입양)
            'ages',
        )
        read_only_fields = (
            'pk',
            'ages',
        )


# 펫을 생성할 때 사용하는 시리얼라이저
class PetCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)  # 이름
    # http://www.django-rest-framework.org/api-guide/fields/#datefield
    birth_date = serializers.DateField(format=api_settings.DATE_FORMAT)  # 생년월일
    # http://www.django-rest-framework.org/api-guide/fields/#choicefield
    gender = serializers.ChoiceField(choices=Pet.CHOICE_GENDER)  # 성별
    body_color = serializers.ChoiceField(choices=Pet.CHOICE_COLOR)  # 색상
    identified_number = serializers.CharField(max_length=20, allow_blank=True) # 동물등록번호
    is_neutering = serializers.BooleanField(default=False)  # 중성화
    is_active = serializers.BooleanField(default=True)  # 활성화
    ages = MultiplePKsHyperlinkedIdentityField(
        view_name='profile:pet-age',
        lookup_fields=['owner_id', 'pk'],
        lookup_url_kwargs=['user_pk', 'pet_pk']
    )  # 나이

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
            'ages',
        )
        read_only_fields = (
            'pk',
            'ages',
        )

    # 출력 형식을 커스터마이징
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'owner': UserSerializer(instance.owner).data,
            'pet': ret
        }

        return data
