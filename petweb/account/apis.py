from typing import NamedTuple

import requests
from django.contrib.auth import authenticate, get_user_model, settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from . import tasks
from .serializers import UserSerializer, SignupSerializer, EditSerializer

User = get_user_model()


# 로그인을 위한 클래스 뷰
class Login(APIView):
    # post method
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        # 장고가 기본으로 제공하는 authenticate
        user = authenticate(
            email=email,
            password=password,
        )
        if user:
            # authenticate가 완료되면 user 정보를 생성한다
            # 'token'키에는 유저가 지니고 있는 토큰 값을 넣는다
            # 튜플로 오기 때문에 'token'과 'token_created'로 언패킹해서 값을 담는다
            # 'user'키에는 유저에 대한 모든 정보를 보내준다
            token, token_created = Token.objects.get_or_create(user=user)
            # 회원가입할 때와 로그인할 때 유저 필드는 동일한 모습을 보여준다
            # Serializer.py의 to_representation 메소드 참조
            data = {
                'token': token.key,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        # authenticate가 실패하면 data에 실패 메시지를 보낸다
        data = {
            'message': '인증에 실패하였습니다'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


# 페이스북 로그인을 위한 클래스 뷰
class FacebookLogin(APIView):
    def post(self, request):
        # request.data에
        # access_token과 user_id가 들어온다
        # debug 결과의 NamedTuple
        class DebugTokenInfo(NamedTuple):
            app_id: str
            type: str
            application: str
            expires_at: int
            is_valid: bool
            issued_at: int
            scopes: list
            user_id: str

        # user info의 NamedTuple
        class UserInfo(NamedTuple):
            id: str
            name: str
            email: str

        # token(access_token)을 받아 해당 토큰을 debug
        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{secret_code}'
            # 액세스 토큰 검사
            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            # 이제 유저 정보가 들어온다
            response = requests.get(url_debug_token, params=params_debug_token)
            return DebugTokenInfo(**response.json()['data'])

        # 유저 정보를 받아온다
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
            return UserInfo(**response.json())

        # request.data로 전달된 access_token값으로 debug 요청 결과를 받아옴
        debug_token_info = get_debug_token_info(request.data['access_token'])
        # access_token 값으로 user_info 결과를 받아옴
        user_info = get_user_info(request.data['access_token'])

        # 페이스북이 전달한 user_id와 프론트에서 전달받은 user_id가 일치하지 않으면 오류 발생
        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 사용자와 전달받은 id값이 일치하지 않음')

        # 디버그 토큰값이 비정상이라면 오류 발생
        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        # 유저에 대한 인증 과정을 거친다
        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 만일 유저가 있다면 serializer data를 리턴한다
        if not user:
            # 유저가 없다면 유저 생성
            user = User.objects.create_facebook_user(
                email=user_info.email,
                nickname=user_info.name,
                user_type=User.USER_TYPE_FACEBOOK,
                social_id=user_info.id,
            )

        # 유저가 있다면 serialize 데터 전달
        return Response(UserSerializer(user).data)


# 회원가입을 위한 클래스 뷰
class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 이메일 전송 프로세스의 시작
            # user = 시리얼라이저된 데이터
            user = serializer.data
            # 현재 사이트의 메인 도메인을 가져온다
            current_site = get_current_site(request)
            # 이메일 수신자: 가입한 회원
            to_email = user['user']['email']
            # 이메일 제목
            subject = '[Pet Service] 회원가입 인증 이메일'
            # 이메일 내용: 템플릿을 렌더링해 전송한다
            message = render_to_string('user_activate_email.html', {
                # 도메인, 바이트 단위로 암호화된 유저 primary key, token이 이메일에 담긴다
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user['user']['pk'])),
                'token': user['token']
            })
            # 이메일 전송 메소드
            # celery tasks가 함수를 실행하도록 tasks.py에 옮겨둠
            tasks.send_mail_task.delay(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                to_email,
            )
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이메일 인증 링크를 클릭하면 활성화되는 뷰
class Activate(APIView):
    # method: get
    def get(self, request, uidb64, token):
        try:
            # 암호화된 user primary key를 복호화
            uid = force_text(urlsafe_base64_decode(uidb64))
            # uid 값으로 user 객체 불러오기
            user = User.objects.get(pk=uid)
        # 예외처리
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # 만일 user가 생성되어 있고
        # url에 담겨온 token 값과 user 객체 안에 담겨 있던 token 값이 일치한다면
        if user is not None and token == Token.objects.get(user=user).key:
            # 유저를 활성화 시킨 뒤 저장한다
            user.is_active = True
            user.save()
            data = {
                'token': token,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': '회원 활성화에 실패하였습니다'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


# 유저 디테일 보기 / 닉네임 수정 / 유저 삭제를 위한 클래스 뷰
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    # 유저 정보 가져오기
    def get_object(self, user_pk):
        return User.objects.get(pk=user_pk)

    # 유저 디테일 보기 (method: get)
    def get(self, request, user_pk):
        user = self.get_object(user_pk)
        serializer = UserSerializer(user)
        data = {
            'token': user.token,
            'user': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    # 유저 닉네임 수정 (method: patch)
    def patch(self, request, user_pk):
        user = self.get_object(user_pk)
        serializer = EditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                'token': user.token,
                'user': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': '업데이트에 실패했습니다'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # 유저 삭제 (method: delete)
    def delete(self, request, user_pk):
        user = self.get_object(user_pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
