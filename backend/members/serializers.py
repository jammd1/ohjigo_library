from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. 프론트엔드에서 어떤 이름으로 보내든(username 또는 sid) 
        # 이를 'username' 키에 담아 장고 인증 시스템에 전달해야 합니다.
        username = attrs.get("username") or attrs.get("sid")
        
        if username:
            # 숫자로 들어오든 문자로 들어오든 일단 문자로 변환
            attrs["username"] = str(username)
            
        # 2. 부모 클래스의 validate를 실행하면 
        # 장고가 USERNAME_FIELD(즉, sid)와 password를 대조합니다.
        data = super().validate(attrs)

        # 3. 로그인 성공 시 토큰 외에 사용자 정보를 같이 내려주면 프론트가 편합니다.
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