from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

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


# 회원가입을 위한 클래스 뷰
class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


# 유저 디테일 보기 / 닉네임 수정 / 유저 삭제를 위한 클래스 뷰
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    # 유저 정보 가져오기
    def get_object(self, pk):
        return User.objects.get(pk=pk)

    # 유저 디테일 보기 (method: get)
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        data = {
            'token': user.token,
            'user': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    # 유저 닉네임 수정 (method: patch)
    def patch(self, request, pk):
        user = self.get_object(pk)
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
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
