from django.contrib.auth import authenticate
from django.test import TransactionTestCase, Client

from .models import User


class UserModelTest(TransactionTestCase):
    DUMMY_EMAIL = 'dummy@email.com'
    DUMMY_NICKNAME = 'nickname'
    DUMMY_PASSWORD = 'password'

    def test_fields_default_value(self):
        # 유저가 정상적으로 생성되는지 테스트
        user = User.objects.create_user(
            email=self.DUMMY_EMAIL,
            nickname=self.DUMMY_NICKNAME,
            password=self.DUMMY_PASSWORD,
        )
        self.assertEqual(user.email, self.DUMMY_EMAIL)
        self.assertEqual(user.nickname, self.DUMMY_NICKNAME)

        self. assertEqual(user, authenticate(
            email=self.DUMMY_EMAIL,
            password=self.DUMMY_PASSWORD,
        ))

    def test_user_login(self):
        # 유저 로그인 테스트
        User.objects.create_user(
            email=self.DUMMY_EMAIL,
            nickname=self.DUMMY_NICKNAME,
            password=self.DUMMY_PASSWORD,
        )
        c = Client()
        response = c.post('/account/login/',
                          {'email': f'{self.DUMMY_EMAIL}',
                           'password': f'{self.DUMMY_PASSWORD}'})
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        # 유저 회원가입 테스트
        c = Client()
        response = c.post('/account/signup/',
                          {'email': f'{self.DUMMY_EMAIL}',
                           'nickname': f'{self.DUMMY_NICKNAME}',
                           'password1': f'{self.DUMMY_PASSWORD}',
                           'password2': f'{self.DUMMY_PASSWORD}'})
        self.assertEqual(response.status_code, 201)

