from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

__all__ = (
    'UserSerializer',
    'SignupSerializer',
    'EditSerializer',
    'ResetPasswordSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    # 유저 로그인 시 결과 필드를 보여주는 모델 시리얼라이저
    class Meta:
        # 유저 모델을 참조한다
        model = User
        # 필드 목록
        fields = (
            'pk',
            'user_type',
            'email',
            'nickname',
            'is_active',
            'date_joined',
            'image',
        )


class SignupSerializer(serializers.ModelSerializer):
    # 유저 가입 시 필드를 생성하는 모델 시리얼라이저
    # 패스워드 1, 2는 추가로 설정해준다
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    nickname = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        # 유저 모델을 참조한다
        model = User
        # 가입 완료 후 나타나는 결과 필드
        fields = (
            'pk',
            'user_type',
            'email',
            'nickname',
            'password1',
            'password2',
            'is_active',
            'date_joined',
            'image',
        )

    # 기본 모델 시리얼라이저는 password1, 2에 대한 validate가 없으므로 만들어준다
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    # 유저를 생성하는 메소드
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password1'],
            image=validated_data.get('image', None),
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


class EditSerializer(serializers.ModelSerializer):
    # 유저 정보 수정을 도와주는 모델 시리얼라이저
    # 닉네임 수정: 반드시 입력될 필요는 없음(allow_blank=True)
    nickname = serializers.CharField(allow_blank=True)
    # 패스워드 수정
    # 입력하더라도 출력값에 변경된 패스워드가 나오지는 않음(write_only=True)
    # 반드시 입력될 필요는 없음(allow_blank=True)
    password1 = serializers.CharField(write_only=True, allow_blank=True)
    password2 = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'user_type',
            'email',
            'nickname',
            'password1',
            'password2',
            'is_active',
            'date_joined',
            'image',
        )

    def validate(self, data):
        # 비밀번호가 입력되었을 경우 비밀번호 1과 2가 같은지 검사한다
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError('Passwords do not match')
        return data

    def update(self, instance, validated_data):
        # 업데이트 함수
        # 닉네임이 변경되었다면 user 인스턴스에 반영한다
        new_nickname = validated_data.get('nickname', None)
        if new_nickname:
            instance.nickname = new_nickname
        # 패스워드는 입력될 수도 있고 안될 수도 있기 때문에 get으로 받아서 변수 'password'에 담아둔다
        new_password = validated_data.get('password1', None)
        # 만일 변경된 패스워드가 입력되었다면
        if new_password:
            # user 인스턴스에 변경된 패스워드를 hash값으로 변환해 입력한다
            instance.set_password(new_password)
        new_image = validated_data.get('image', None)
        if new_image:
            instance.image = new_image
        # 변경된 모든 데이터를 저장한다
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        user_email = data['email']
        if not User.objects.filter(email=user_email).exists():
            raise serializers.ValidationError('Email does not exist.')
        return data
