from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from . import tasks
from .serializers import UserSerializer, SignupSerializer, EditSerializer
from config.settings.base import *

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
                EMAIL_HOST_USER,
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
