from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from .apis import Signup

User = get_user_model()


class UserSignupTest(APILiveServerTestCase):
    # DB를 쓸 때는 LiveServerTestCase 사용
    URL_API_SIGNUP_NAME = 'account:signup'
    URL_API_SIGNUP = '/account/signup/'
    VIEW_CLASS = Signup

    # 유저 생성 메소드
    @staticmethod
    def create_user(email='dummy@email.com'):
        return User.objects.create_user(email=email, nickname='dummy')

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

    # 테스트 3. 생성한 유저가 DB에 존재하는가
    def test_user_is_exist(self):
        dummy_user = self.create_user()
        dummy_pk = dummy_user.pk
        query = User.objects.filter(pk=dummy_pk)
        self.assertTrue(query.exists())

    # 테스트 4. 페이스북 유저가 생성되고 DB에 존재하는가
    def test_facebook_user_is_exist(self):
        dummy_facebook_user = self.create_facebook_user()
        dummy_pk = dummy_facebook_user.pk
        query = User.objects.filter(pk=dummy_pk)
        self.assertTrue(query.exists())
