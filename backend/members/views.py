from rest_framework import viewsets, generics, permissions
from .models import Member
from .serializer import MemberSerializer, UserCreateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegistrationView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]  # 누구나 회원가입 가능

