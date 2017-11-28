from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        주어진 정보로 일반 User 인스턴스 생성
        """
        if not email:
            # 이메일 정보가 들어오지 않으면 오류 발생
            raise ValueError('이메일 정보는 반드시 필요합니다')

        user = self.model(
            # 유저에 들어갈 정보: 이메일, 닉네임
            email=self.normalize_email(email),
            nickname=nickname,
        )
        user.set_password(password)
        # 패스워드 세팅
        user.save(using=self._db)
        # 유저를 DB에 세이브
        return user

    def create_facebook_user(self, email, nickname, user_type, social_id):
        """
        주어진 정보로 facebook_user 인스턴스 생성
        """
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            user_type=user_type,
            social_id=social_id,
        )
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        """
        주어진 정보로 관리자 권한 User 인스턴스 생성
        """
        user = self.create_user(
            # create_user 함수를 호출해 user 생성
            email=email,
            password=password,
            nickname=nickname,
        )

        user.is_superuser = True
        # 관리자 권한 부여
        user.is_active = True
        user.save(using=self._db)
        # DB에 저장
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # 소셜 유저 타입 정의
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_GOOGLE = 'g'
    USER_TYPE_DJANGO = 'd'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'facebook'),
        (USER_TYPE_GOOGLE, 'google'),
        (USER_TYPE_DJANGO, 'django'),
    )
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE, default=USER_TYPE_DJANGO)
    # 이메일 필드
    email = models.EmailField(
        verbose_name='이메일 주소',
        max_length=255,
        unique=True,
        blank=True,
    )
    social_id = models.CharField(
        verbose_name='소셜 아이디',
        max_length=255,
        blank=True,
    )
    # 닉네임 필드
    nickname = models.CharField(
        verbose_name='닉네임',
        max_length=255,
        unique=True,
    )
    # 활성화 여부 필드
    is_active = models.BooleanField(
        verbose_name='활성화',
        default=False
    )
    # 가입 날짜 필드
    date_joined = models.DateTimeField(
        verbose_name='가입 날짜',
        # 현재 시간 기준
        default=timezone.now
    )

    # 관리자 매니저 지정
    objects = UserManager()

    # 유저 네임을 이메일 계정으로 세팅
    USERNAME_FIELD = 'email'
    # 반드시 필요한 필드 = 닉네임
    REQUIRED_FIELDS = ['nickname', ]

    class Meta:
        # 어드민 페이지에서 보여줄 설명 필드
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
        # 보여주는 순서: 가입 일시
        ordering = ('-date_joined',)

    def __str__(self):
        # 매직 메소드: 유저 이름은 닉네임으로
        return self.nickname

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    @property
    def token(self):
        # signup 후 토큰값을 받는다
        return Token.objects.get_or_create(user=self)[0].key

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_superuser
