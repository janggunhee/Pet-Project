from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.settings import api_settings
from rest_framework.utils import model_meta
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..relations import MultiplePKsHyperlinkedIdentityField
from ..models import Pet, PetSpecies, PetBreed
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSpeciesField',
    'PetBreedField',
    'PetSerializer',
    'PetCreateSerializer',
    'PetEditSerializer',
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
    # thumbnail 이미지 처리
    image = VersatileImageFieldSerializer(
        sizes=[('thumbnail', 'crop__300x300'), ]
    )

    # 펫 종류는 PetSpeciesSerializer로 가공된다
    species = PetSpeciesField()
    # 펫 품종은 PetBreedSerializer로 가공된다
    breeds = PetBreedField()

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
        # 썸네일 이미지
        fields += (
            'image',
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


# 펫 정보를 수정하는 시리얼라이저
class PetEditSerializer(serializers.ModelSerializer):
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
    identified_number = serializers.CharField(max_length=20)  # 동물등록번호
    is_neutering = serializers.BooleanField()  # 중성화
    is_active = serializers.BooleanField()  # 활성화
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

    # 입력 형식을 커스터마이징
    def to_internal_value(self, data):
        # 입력한 데이터(dict 형식)를 key와 value로 나누어 순회한다
        result = {}
        for key, value in data.items():
            # 만일 value가 없다면, 즉 사용자가 변경 사항을 아무것도 입력하지 않았다면
            if not value:
                # 원래 객체가 가지고 있던 값을 입력한다
                result[key] = getattr(self.instance, f'{key}')
            else:
                # 만일 변경 사항이 있다면 그 값을 입력한다
                result[key] = value

        return result

    # 업데이트 메소드 커스터마이징
    def update(self, instance, validated_data):
        # 원래 update 메소드를 긁어와서 커스텀
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # validated_data를 키와 값으로 나누어 순회한다
        for attr, value in validated_data.items():
            # 만일 attr 값이 species고 value의 type이 문자열이라면
            # 즉, 사용자가 값을 바꾸려고 한다면
            if attr == 'species' and type(value) == str:
                # 사용자가 바꾸려고 하는 값의 펫 종류 객체를 가져온다
                pet_species_instance = PetSpecies.objects.get(pet_type=value)
                # 펫 인스턴스의 species 값을 새로운 펫 종류 객체로 교체한다
                # https://docs.python.org/3/library/functions.html#setattr
                setattr(instance, attr, pet_species_instance)
            # 만일 attr 값이 breeds고 value의 type이 문자열이라면
            elif attr == 'breeds' and type(value) == str:
                # 사용자가 바꾸려고 하는 값의 펫 품종 객체를 가져온다
                pet_breed_instance = PetBreed.objects.get(breeds_name=value)
                # 펫 인스턴스의 breeds 값을 새로운 펫 품종 객체로 교체한다
                setattr(instance, attr, pet_breed_instance)
            # 나머지는 update 원래 메소드 가져옴
            elif attr in info.relations and info.relations[attr].to_many:
                # https://docs.python.org/3/library/functions.html#getattr
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


# 사용자가 강아지/고양이를 선택하면 펫 품종을 보여주는 시리얼라이저
class PetBreedSerializer(serializers.ModelSerializer):
    species = PetSpeciesField(write_only=True)

    class Meta:
        model = PetBreed
        fields = (
            'species',
            'breeds_name',
        )
