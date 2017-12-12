from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APILiveServerTestCase

from ..serializers import SignupSerializer
from ..apis import Signup, Login, UserProfileUpdateDestroy, Logout

User = get_user_model()


__all__ = (
    'DummyUser',
    'UserSignupTest',
    'UserLoginTest',
    'UserLogoutTest',
    'UserProfileTest',
)


# 자주 쓰는 메소드를 클래스로 정의
class DummyUser:
    @staticmethod
    def create_user(email='dummy2@email.com'):
        user = User.objects.create_user(email=email, nickname='dummy2', password='123456789')
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def create_facebook_user(email='facebookdummy@email.com'):
        return User.objects.create_facebook_user(
            email=email,
            nickname='facebook_dummy',
            user_type=User.USER_TYPE_FACEBOOK,
            social_id='dummy_number',
        )


# 유저 회원가입 테스트
class UserSignupTest(APILiveServerTestCase):
    # DB를 쓸 때는 LiveServerTestCase 사용
    def setUp(self):
        self.URL_API_SIGNUP_NAME = 'auth:signup'
        self.URL_API_SIGNUP = '/auth/signup/'
        self.SIGNUP_VIEW_CLASS = Signup

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
            self.SIGNUP_VIEW_CLASS
        )

    # 테스트 3. signup url로 user가 생성되는가
    def test_signup_dummy_user(self):
        # 더미 유저 데이터 생성
        input_data = {
            'email': 'dummy1@email.com',
            'nickname': 'pycharm_dummy',
            'password1': '123456789',
            'password2': '123456789'

        }
        # signup url에 더미 유저 데이터로 회원가입 요청
        response = self.client.post(self.URL_API_SIGNUP, data=input_data)
        # 회원가입이 201 코드로 성사되었는지 검사
        self.assertEqual(response.status_code, 201)
        # 생성된 더미 유저
        dummy_user = User.objects.get(email=input_data['email'])
        # 더미 유저를 시리얼라이징
        serializer = SignupSerializer(dummy_user).data
        # 토큰 가져오기
        dummy_token = Token.objects.get(user__email=input_data['email'])
        # 토큰 일치 검사
        self.assertEqual(serializer['token'], dummy_token.key)
        # 처음 입력한 이메일과 DB에 저장된 이메일이 일치하는지 검사
        self.assertEqual(serializer['user']['email'], input_data['email'])
        # 처음 입력한 닉네임과 DB에 저장된 닉네임이 일치하는지 검사
        self.assertEqual(serializer['user']['nickname'], input_data['nickname'])

    # # 테스트 4. 페이스북 유저가 생성되고 DB에 존재하는가
    # def test_facebook_user_is_exist(self):
    #     dummy_facebook_user = DummyUser.create_facebook_user()
    #     dummy_pk = dummy_facebook_user.pk
    #     query = User.objects.filter(pk=dummy_pk)
    #     self.assertTrue(query.exists())


# 유저 로그인 테스트
class UserLoginTest(APILiveServerTestCase):
    def setUp(self):
        # URL
        self.URL_API_LOGIN_NAME = 'auth:login'
        self.URL_API_LOGIN = '/auth/login/'
        self.LOGIN_VIEW_CLASS = Login

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
            self.LOGIN_VIEW_CLASS
        )

    # 테스트 7. login url로 유저가 로그인 되는가
    def test_user_login(self):
        dummy_user = DummyUser.create_user()
        data = {
            'email': 'dummy2@email.com',
            'password': '123456789'
        }
        response = self.client.post(self.URL_API_LOGIN, data=data)
        self.assertEqual(response.status_code, 200)


# 유저 로그아웃 테스트
class UserLogoutTest(APILiveServerTestCase):
    def setUp(self):
        # URL
        self.URL_API_LOGOUT_NAME = 'auth:logout'
        self.URL_API_LOGOUT = '/auth/logout/'
        self.LOGOUT_VIEW_CLASS = Logout

    # 테스트 8. logout url이 reverse name과 일치하는가
    def test_logout_url_name_reverse(self):
        url = reverse(self.URL_API_LOGOUT_NAME)
        self.assertEqual(url, self.URL_API_LOGOUT)

    # 테스트 9. account.apis.Logout view에 대해
    # URL, reverse, resolve, view 함수가 같은지 확인
    def test_logout_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_LOGOUT)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_LOGOUT_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.LOGOUT_VIEW_CLASS
        )

    # 테스트 10. login url로 유저가 로그아웃 되는가
    def test_user_logout(self):
        dummy_user = DummyUser.create_user()
        dummy_token = dummy_user.token
        # http_authorization 인증
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + dummy_token)

        response = self.client.post(self.URL_API_LOGOUT)
        self.assertEqual(response.status_code, 200)


# 유저 프로필 테스트 (디테일/정보 수정/삭제)
class UserProfileTest(APILiveServerTestCase):
    def setUp(self):
        # URL
        self.dummy_user_pk = '1'
        self.URL_API_PROFILE_NAME = 'profile:user'
        self.URL_API_PROFILE_DUMMY = '/profile/' + self.dummy_user_pk + '/'
        self.URL_API_PROFILE = '/profile/'
        self.PROFILE_VIEW_CLASS = UserProfileUpdateDestroy

    # 테스트 11. profile url이 reverse name과 일치하는가
    def test_detail_url_name_reserve(self):
        url = reverse(self.URL_API_PROFILE_NAME, args=self.dummy_user_pk, )
        self.assertEqual(url, self.URL_API_PROFILE_DUMMY)

    # 테스트 12. account.apis.Detail view에 대해
    # URL, reverse, resolve, view 함수가 같은지 확인
    def test_detail_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_PROFILE_DUMMY)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_PROFILE_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.PROFILE_VIEW_CLASS
        )

    # 테스트 13. profile url에 접속 가능한가
    def test_user_connect_profile_view(self):
        dummy_user = DummyUser.create_user()
        token = dummy_user.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.URL_API_PROFILE + str(dummy_user.pk) + '/')
        self.assertEqual(response.status_code, 200)

    # 테스트 14. profile url로 닉네임 변경
    def test_user_nickname_modify(self):
        dummy_user = DummyUser.create_user()
        token = dummy_user.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            'nickname': 'hello',
            'password1': '',
            'password2': '',
        }
        response = self.client.patch(self.URL_API_PROFILE + str(dummy_user.pk) + '/', data=data)
        # 응답 코드가 정상인가
        self.assertEqual(response.status_code, 200)
        # 바뀐 유저의 인스턴스를 찾는다
        patched_user = User.objects.get(auth_token=token)
        # 바뀐 유저의 닉네임이 우리가 입력한 값과 같은가
        self.assertEqual(patched_user.nickname, data['nickname'])

    # 테스트 15. profile url로 패스워드 변경
    def test_user_password_modify(self):
        dummy_user = DummyUser.create_user()
        token = dummy_user.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            'nickname': '',
            'password1': '654321',
            'password2': '654321',
        }
        response = self.client.patch(self.URL_API_PROFILE + str(dummy_user.pk) + '/', data=data)
        # 응답 코드가 정상인가
        self.assertEqual(response.status_code, 200)
        # 바뀐 유저의 인스턴스를 찾는다
        patched_user = User.objects.get(auth_token=token)
        # 바뀐 유저의 이메일과 패스워드로 로그인이 가능한가
        login = self.client.login(email=patched_user.email, password=data['password1'])
        self.assertTrue(login)

    # 테스트 16. profile url로 유저 삭제
    def test_user_delete(self):
        dummy_user = DummyUser.create_user()
        token = dummy_user.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete(self.URL_API_PROFILE + str(dummy_user.pk) + '/')
        self.assertEqual(response.status_code, 204)
