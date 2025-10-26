from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        # 중요: password와 같은 민감한 정보는 API에 노출되지 않도록 제외합니다.
        fields = ['sid', 'name', 'email', 'status', 'join_date']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'password']

    def create(self, validated_data):
        user = Member.objects.create_user(
            sid=validated_data['sid'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 사용자 지정 클레임 추가 (토큰 자체에 정보를 담음)
        token['sid'] = user.sid
        token['name'] = user.name
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # 기본 응답 데이터에 사용자 정보 추가 (로그인 응답 바디에 정보를 담음)
        data['sid'] = self.user.sid
        data['name'] = self.user.name
        data['email'] = self.user.email
        return data


