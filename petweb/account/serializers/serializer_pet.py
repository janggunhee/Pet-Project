from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Pet
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSerializer',
)


class PetSerializer(serializers.ModelSerializer):
    # 펫에 관한 결과를 보여주는 시리얼라이저
    # 주인을 pk값만 보여주는 대신 시리얼라이저된 결과로 보여주기 위한 옵션
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
