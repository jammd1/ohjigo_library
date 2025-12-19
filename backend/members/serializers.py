from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    sid = serializers.IntegerField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['sid'] = int(user.sid)
        token['name'] = user.name
        token['role'] = user.role 
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['sid'] = self.user.sid
        data['name'] = self.user.name
        data['email'] = self.user.email
        data['role'] = self.user.role 
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # MemberManager의 create_user를 호출할 때 username을 명시적으로 넘깁니다.
        user = Member.objects.create_user(
            sid=validated_data['sid'],
            username=str(validated_data['sid']), # 이 부분이 로그인 가능 여부를 결정합니다.
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'UNDERGRADUATE')
        )
        return user

# CustomTokenObtainPairSerializer 및 MemberSerializer는 기존과 동일하게 유지