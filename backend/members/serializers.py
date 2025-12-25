from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 이 클래스가 UserCreateSerializer 위에나 아래에 꼭 있어야 합니다!
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 프론트엔드에서 'sid'로 보내는 경우를 대비해 필드를 동적으로 추가합니다.
        self.fields['sid'] = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs):
        # 1. 'username'이 비어있고 'sid'가 들어왔다면 'username'에 채워줍니다.
        if not attrs.get("username") and attrs.get("sid"):
            attrs["username"] = str(attrs.get("sid"))
        
        # 2. 혹시 몰라 한 번 더 문자열로 변환 (타입 에러 방지)
        if attrs.get("username"):
            attrs["username"] = str(attrs.get("username"))

        # 3. 이제 부모 클래스가 'username'을 가지고 인증을 진행합니다.
        data = super().validate(attrs)

        # 로그인 성공 시 추가 정보 반환
        data['name'] = self.user.name
        data['sid'] = self.user.sid
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