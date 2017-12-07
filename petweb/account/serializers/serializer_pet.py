from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils import pet_age
from ..models import Pet, PetSpecies, PetBreed
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSerializer',
    'EditPetSerializer',
)


class PetSerializer(serializers.ModelSerializer):
    # 펫에 관한 결과를 보여주는 시리얼라이저
    # 주인을 pk값만 보여주는 대신 시리얼라이저된 결과로 보여주기 위한 옵션
    # read_only=True는 입력되어야 할 값이 불완전하더라도 알아서 메워줌
    # pet create 할 때 필요한 옵션
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = (
            'owner',  # 주인
            'pk',    # 동물pk
            'species',  # 강아지/고양이
            'breeds',  # 품종
            'name',  # 이름
            'birth_date',  # 생년월일
            'gender',  # 성별
            'identified_number',  # 동물등록번호
            'is_neutering',  # 중성화
            'body_color',  # 색깔
            'is_active'  # 활성화여부(동물사망/양도/입양)
        )
        read_only_fields = (
            'owner',
            'pk',
        )


class EditPetSerializer(serializers.ModelSerializer):
    # 펫의 정보 수정용 시리얼라이저

    class Meta:
        model = Pet
        fields = (
            'owner',  # 주인
            'pk',  # 동물pk
            'species',  # 강아지/고양이
            'breeds',  # 품종
            'name',  # 이름
            'birth_date',  # 생년월일
            'gender',  # 성별
            'identified_number',  # 동물등록번호
            'is_neutering',  # 중성화
            'body_color',  # 색깔
            'is_active'  # 활성화여부(동물사망/양도/입양)
        )
        read_only_fields = (
            'owner',
            'pk',
        )
