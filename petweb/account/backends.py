from django.contrib.auth import get_user_model

User = get_user_model()


# 페이스북
class FacebookBackend(object):
    """
    페이스북 로그인 시 페이스북 아이디를 검증하는 클래스
    """
    def authenticate(self, request, facebook_user_id):
        try:
            return User.objects.get(social_id=facebook_user_id)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
