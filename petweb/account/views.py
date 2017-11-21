from django.contrib.auth import authenticate, get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, SignupSerializer

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


# 회원 가입을 위한 클래스 뷰
class Signup(APIView):
    # post method
    def post(self, request):
        # SignupSerializer를 사용하여 유효성을 검증한다
        serializer = SignupSerializer(data=request.data)
        # 유효성 검증에 통과하면 DB에 저장한다
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 실패하면 400 에러를 띄운다
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴를 위한 클래스 뷰
class Delete(APIView):
    queryset = User.objects.all()

    # 삭제할 유저 인스턴스를 가져오는 메소드
    def get_object(self):
        try:
            instance = self.queryset.get(email=self.request.user.email)
            return instance
        except User.DoesNotExist:
            raise Http404

    # 인스턴스 삭제 메소드
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
