from rest_framework import viewsets, generics, permissions, serializers
from .models import Member
# MemberSerializer와 UserCreateSerializer 둘 다 import
from .serializer import MemberSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

# 👇👇👇 [수정] 이 클래스를 통째로 덮어쓰세요. 👇👇👇
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer # 기본 시리얼라이저
    lookup_field = 'sid'

    # 5. (핵심) 이 함수가 'create' 액션일 때
    #    UserCreateSerializer를 반환하도록 합니다.
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()


# Define a simple serializer just for the schema documentation
class TokenObtainRequestSerializer(serializers.Serializer):
    sid = serializers.IntegerField()
    password = serializers.CharField()

@extend_schema(
    request=TokenObtainRequestSerializer,
    summary="Custom Token Obtain",
    description="Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials."
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]  # 누구나 회원가입 가능