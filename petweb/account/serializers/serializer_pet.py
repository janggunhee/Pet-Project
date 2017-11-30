from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Pet
from . import UserSerializer

User = get_user_model()

__all__ = (
    'PetSerializer',
)


class PetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    # species = serializers.CharField

    class Meta:
        model = Pet
        fields = (
            'owner',
            'pk',
            'species',
            'breeds',
            'name',
            'birth_date',
            'gender',
            'identified_number',
            'is_neutering',
            'body_color',
        )
