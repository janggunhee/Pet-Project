from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 유저 로그인 시 결과 필드를 보여주는 모델 시리얼라이저
    class Meta:
        # 유저 모델을 참조한다
        model = User
        # 필드 목록
        fields = (
            'id',
            'user_type',
            'email',
            'nickname',
            'is_active',
            'date_joined',
        )


class SignupSerializer(serializers.ModelSerializer):
    # 유저 가입 시 필드를 생성하는 모델 시리얼라이저
    # 패스워드 1, 2는 추가로 설정해준다
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        # 유저 모델을 참조한다
        model = User
        # 가입 완료 후 나타나는 결과 필드
        fields = (
            'id',
            'user_type',
            'email',
            'nickname',
            'password1',
            'password2',
            'is_active',
            'date_joined',
        )

    # 기본 모델 시리얼라이저는 password1, 2에 대한 validate가 없으므로 만들어준다
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다')
        return data

    # 유저를 생성하는 메소드
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password1'],
        )

    # 출력되는 json을 우리가 원하는 형태로 커스터마이징
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # super().to_representation()은 기본 json 형태
        # 회원가입할 때와 로그인할 때 유저 필드는 동일한 모습을 보여준다
        # views.py의 Login 클래스 참조
        data = {
            # 모델에 property 값으로 token을 생성해두었다
            'token': instance.token,
            'user': ret,
        }
        return data
