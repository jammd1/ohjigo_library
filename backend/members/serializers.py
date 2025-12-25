from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 1. 프론트엔드에서 보내는 'sid'를 공식적으로 허용합니다. (이게 핵심입니다)
    sid = serializers.CharField(required=True)
    # 2. 부모가 기본으로 요구하는 'username'은 잠시 필수 해제합니다.
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        # 3. 프론트에서 준 'sid' 값을 뽑아서 'username' 자리에 넣어줍니다.
        # SimpleJWT는 내부적으로 'username'이라는 이름의 데이터가 있어야 로그인을 진행합니다.
        sid_value = attrs.get('sid')
        if sid_value:
            attrs['username'] = sid_value
        
        # 4. 부모(SimpleJWT)의 원래 검증 로직을 실행합니다.
        # 여기서 'sid'가 남아있으면 에러가 날 수 있으니 슬쩍 지워줍니다.
        temp_attrs = attrs.copy()
        if 'sid' in temp_attrs:
            del temp_attrs['sid']
            
        # 5. 이제 깨끗해진 데이터로 실제 로그인을 시도합니다.
        data = super().validate(temp_attrs)

        # 6. 로그인 성공 후 프론트에 돌려줄 데이터
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