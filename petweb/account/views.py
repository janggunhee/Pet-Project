from typing import NamedTuple

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from config import settings


# 첫 화면
def index(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'facebook_secret_code': settings.FACEBOOK_APP_SECRET_CODE,
        'facebook_user_scope': settings.FACEBOOK_SCOPE
    }
    return render(request, 'index.html', context)


# 프론트엔드 페이스북 로그인을 파이썬으로 구현
# facebook_user_id와 access_token을 리턴
class FrontFacebookLogin(View):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        type: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        user_id: str

    class UserInfo(NamedTuple):
        id: str
        name: str
        email: str

    def get(self, request):
        # https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#checklogin
        # 로그인 대화 상자 호출한 뒤 리디렉션된 URL
        # 페이스북 로그인 시도를 하면 code를 보내준다
        # 이 code와 secret 코드를 재전송해 access token을 받아온다
        app_id = settings.FACEBOOK_APP_ID
        secret_code = settings.FACEBOOK_APP_SECRET_CODE
        app_access_token = f'{app_id}|{secret_code}'
        # 페이스북이 전달해준 코드
        code = request.GET.get('code')

        def get_access_token_info(code_value):
            # {{ request.scheme }}://{{ request.META.HTTP_HOST }}{% url 'account:facebook-login' %}
            redirect_uri = '{scheme}://{host}{relative_url}'.format(
                scheme=request.scheme,
                host=request.META['HTTP_HOST'],
                relative_url=reverse('account:front-facebook-login'),
            )
            # 액세스 토큰을 요청하기 위한 엔드포인트
            url_access_token = 'https://graph.facebook.com/v2.11/oauth/access_token'
            # 액세스 토큰을 요청할 때 GET parameter 목록
            params_access_token = {
                'client_id': app_id,
                'redirect_uri': redirect_uri,
                'client_secret': secret_code,
                'code': code_value,
            }
            """
            결과 예시:
            {
              "access_token": {access-token}, 
              "token_type": {type},
              "expires_in":  {seconds-til-expiration}
            }
            """
            response = requests.get(url_access_token, params=params_access_token)
            # 위에서 생성한 네임드튜플에 출력된 값을 넣는다
            return self.AccessTokenInfo(**response.json())

        def get_debug_token_info(token):
            # 액세스 토큰 검사
            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            # 이제 유저 정보가 들어온다
            response = requests.get(url_debug_token, params=params_debug_token)
            return self.DebugTokenInfo(**response.json()['data'])

        def get_user_info(token):
            # 유저 정보를 받아온다
            user_info_fields = [
                'id',
                'name',
                'email',
            ]
            url_graph_user_info = 'https://graph.facebook.com/me'
            params = {
                'fields': ','.join(user_info_fields),
                'access_token': token
            }
            response = requests.get(url_graph_user_info, params=params)
            return self.UserInfo(**response.json())

        # 액세스 토큰을 받아오는 프로세스를 내장함수로 만들고
        # 내장함수를 변수로 사용한다
        token_info = get_access_token_info(code)
        # 네임드튜플에서 액세스 토큰을 꺼낸다
        access_token_info = token_info.access_token
        # 디버그 토큰을 받아온다
        debug_token_info = get_debug_token_info(access_token_info)
        # 유저 정보를 받아온다
        user_info = get_user_info(access_token_info)

        data = {
            'facebook_user_id': user_info.id,
            'access_token': access_token_info,
        }

        return JsonResponse(data)
