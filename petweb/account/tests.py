from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from .apis import Signup

User = get_user_model()

# class UserModelTest(TransactionTestCase):
#     DUMMY_EMAIL = 'dummy@email.com'
#     DUMMY_NICKNAME = 'nickname'
#     DUMMY_PASSWORD = 'password'
#
#     def test_fields_default_value(self):
#         # 유저가 정상적으로 생성되는지 테스트
#         user = User.objects.create_user(
#             email=self.DUMMY_EMAIL,
#             nickname=self.DUMMY_NICKNAME,
#             password=self.DUMMY_PASSWORD,
#         )
#         self.assertEqual(user.email, self.DUMMY_EMAIL)
#         self.assertEqual(user.nickname, self.DUMMY_NICKNAME)
#
#         self. assertEqual(user, authenticate(
#             email=self.DUMMY_EMAIL,
#             password=self.DUMMY_PASSWORD,
#         ))
#
#     def test_user_login(self):
#         # 유저 로그인 테스트
#         User.objects.create_user(
#             email=self.DUMMY_EMAIL,
#             nickname=self.DUMMY_NICKNAME,
#             password=self.DUMMY_PASSWORD,
#         )
#         c = Client()
#         response = c.post('/account/login/',
#                           {'email': f'{self.DUMMY_EMAIL}',
#                            'password': f'{self.DUMMY_PASSWORD}'})
#         self.assertEqual(response.status_code, 200)
#
#     def test_user_signup(self):
#         # 유저 회원가입 테스트
#         c = Client()
#         response = c.post('/account/signup/',
#                           {'email': f'{self.DUMMY_EMAIL}',
#                            'nickname': f'{self.DUMMY_NICKNAME}',
#                            'password1': f'{self.DUMMY_PASSWORD}',
#                            'password2': f'{self.DUMMY_PASSWORD}'})
#         self.assertEqual(response.status_code, 201)
#


class UserSignupTest(APILiveServerTestCase):
    # DB를 쓸 때는 LiveServerTestCase 사용
    URL_API_SIGNUP_NAME = 'account:signup'
    URL_API_SIGNUP = '/account/signup/'
    VIEW_CLASS = Signup

    # 유저 생성 메소드
    @staticmethod
    def create_user(email='dummy@email.com'):
        return User.objects.create_user(email=email, nickname='dummy')

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

    # 테스트 3. 생성한 유저가 DB에 존재하는가
    def test_user_is_exist(self):
        dummy_user = self.create_user()
        dummy_pk = dummy_user.pk
        query = User.objects.filter(pk=dummy_pk)
        self.assertTrue(query.exists())

    # 테스트 4. 유저를 생성해 이메일이 전송되는지 확인한다
    def test_send_email(self):
        c = Client()
        response = c.post(self.URL_API_SIGNUP,
                          {'email': 'dummy@email.com',
                           'nickname': 'dummy',
                           'password1': '1234',
                           'password2': '1234'})
        self.assertEqual(response.status_code, 201)

