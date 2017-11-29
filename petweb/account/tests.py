from pprint import pprint

from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.test import Client
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APILiveServerTestCase, APIRequestFactory, APIClient

from account.serializers import UserSerializer, SignupSerializer
from .apis import Signup, Login

User = get_user_model()


class UserSignupTest(APILiveServerTestCase):
    # DB를 쓸 때는 LiveServerTestCase 사용
    URL_API_SIGNUP_NAME = 'account:signup'
    URL_API_SIGNUP = '/account/signup/'
    VIEW_CLASS = Signup

    @staticmethod
    def create_facebook_user(email='facebookdummy@email.com'):
        return User.objects.create_facebook_user(
            email=email,
            nickname='facebook_dummy',
            user_type=User.USER_TYPE_FACEBOOK,
            social_id='dummy_number',
        )

    # 테스트 1. signup url이 reverse name과 매치되는가
    def test_signup_url_name_reverse(self):
        url = reverse(self.URL_API_SIGNUP_NAME)
        self.assertEqual(url, self.URL_API_SIGNUP)

    # 테스트 2. account.apis.Signup view에 대해
    # URL, reverse, resolve, view 함수가 같은지 확인
    def test_signup_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_SIGNUP)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_SIGNUP_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS
        )

    # 테스트 3. signup url로 user가 생성되는가
    def test_signup_dummy_user(self):
        # 더미 유저 데이터 생성
        data = {
            'email': 'dummy1@email.com',
            'nickname': 'pycharm_dummy',
            'password1': '123456789',
            'password2': '123456789'

        }
        # signup url에 더미 유저 데이터로 회원가입 요청
        response = self.client.post(self.URL_API_SIGNUP, data)
        # 회원가입이 201 코드로 성사되었는지 검사
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 생성된 더미 유저
        dummy_user = User.objects.get(email='dummy1@email.com')
        # 더미 유저를 시리얼라이징
        serializer = SignupSerializer(dummy_user).data
        # 콘솔 창에 회원가입 결과를 띄워 줌
        result = pprint(serializer)
        # 토큰 일치 검사
        self.assertEqual(serializer['token'], dummy_user.token)
        # 처음 입력한 이메일과 DB에 저장된 이메일이 일치하는지 검사
        self.assertEqual(serializer['user']['email'], data['email'])
        # 처음 입력한 닉네임과 DB에 저장된 닉네임이 일치하는지 검사
        self.assertEqual(serializer['user']['nickname'], data['nickname'])

    # 테스트 4. 페이스북 유저가 생성되고 DB에 존재하는가
    def test_facebook_user_is_exist(self):
        dummy_facebook_user = self.create_facebook_user()
        dummy_pk = dummy_facebook_user.pk
        query = User.objects.filter(pk=dummy_pk)
        self.assertTrue(query.exists())


class UserLoginTest(APILiveServerTestCase):
    URL_API_LOGIN_NAME = 'account:login'
    URL_API_LOGIN = '/account/login/'
    VIEW_CLASS = Login
    client = APIClient()

    # 유저 생성 메소드
    @staticmethod
    def create_user(email='dummy2@email.com'):
        return User.objects.create_user(email=email, nickname='dummy2', password='123456789')

    # 테스트 5. login url이 reverse name과 일치하는가
    def test_login_url_name_reverse(self):
        url = reverse(self.URL_API_LOGIN_NAME)
        self.assertEqual(url, self.URL_API_LOGIN)

    # 테스트 6. account.apis.Login view에 대해
    # URL, reverse, resolve, view 함수가 같은지 확인
    def test_login_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_LOGIN)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_LOGIN_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS
        )
