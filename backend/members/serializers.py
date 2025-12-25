from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 프론트 Payload 확인 결과, 데이터가 'username'으로 오고 있습니다.
    # 따라서 sid 선언을 지우고 기본 username 로직을 따릅니다.
    
    def validate(self, attrs):
        # 1. 부모 클래스(SimpleJWT)의 기본 검증을 먼저 실행합니다.
        # SimpleJWT는 기본적으로 'username'과 'password'를 검사합니다.
        data = super().validate(attrs)

        # 2. 검증이 성공하면(로그인 성공), 응답에 필요한 정보를 추가합니다.
        # self.user를 통해 DB에서 추가 정보를 가져옵니다.
        data['name'] = self.user.name
        data['sid'] = self.user.sid
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