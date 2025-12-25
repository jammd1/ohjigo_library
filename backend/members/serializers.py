from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

# members/serializers.py

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 프론트에서 'username'으로 보내는 값을 'sid'로 매핑하기 위해 필드를 정의합니다.
    username_field = Member.USERNAME_FIELD # 'sid'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 기본적으로 SimpleJWT는 USERNAME_FIELD(sid)를 찾습니다.
        # 프론트에서 'username'이라는 키로 데이터를 보내고 있으므로, 
        # 시리얼라이저의 필드 구성을 강제로 username으로 맞춰줍니다.
        self.fields[self.username_field] = serializers.CharField()
        if 'username' in self.initial_data:
            self.initial_data[self.username_field] = self.initial_data.pop('username')[0] if isinstance(self.initial_data.get('username'), list) else self.initial_data.get('username')

    def validate(self, attrs):
        # attrs['sid'] 에 값이 정상적으로 들어왔는지 확인하고 검증을 진행합니다.
        data = super().validate(attrs)

        # 로그인 성공 후 응답 데이터 추가
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