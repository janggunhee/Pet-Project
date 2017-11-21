from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'user_type',
            'email',
            'nickname',
            'is_active',
            'date_joined',
        )
