from rest_framework import viewsets, generics, permissions, serializers
from .models import Member
from .serializer import MemberSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'sid'


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