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


class PetSpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetSpecies
        fields = ('pet_type', )

    def to_representation(self, instance):
        return instance.pet_type


class PetBreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetBreed
        fields = ('breeds_name', )

    def to_representation(self, instance):
        return instance.breeds_name


class PetSerializer(serializers.ModelSerializer):
    # 펫에 관한 결과를 보여주는 시리얼라이저
    species = PetSpeciesSerializer()
    breeds = PetBreedSerializer()
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
        )


class PetCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    # http://www.django-rest-framework.org/api-guide/fields/#datefield
    birth_date = serializers.DateField(format=api_settings.DATE_FORMAT)
    # http://www.django-rest-framework.org/api-guide/fields/#choicefield
    gender = serializers.ChoiceField(choices=Pet.CHOICE_GENDER)
    body_color = serializers.ChoiceField(choices=Pet.CHOICE_COLOR)
    is_neutering = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)

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
        )
        read_only_fields = (
            'pk',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'owner': UserSerializer(instance.owner).data,
            'pet': ret
        }

        return data
