from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        # ★ [수정 1] 마이페이지 등에서 신분을 보려면 여기에 'role'도 추가해야 합니다.
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        # 여기 fields에 role 넣으신 건 아주 잘하셨습니다!
        fields = ['sid', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # ★ [수정 2] 여기서 role 데이터를 꺼내서 넘겨줘야 합니다!
        # (만약 role을 선택 안 했으면 None이 되거나 에러가 날 수 있으니 .get 사용 권장)
        user = Member.objects.create_user(
            sid=validated_data['sid'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'UNDERGRADUATE') # ★ 핵심: role 전달
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    sid = serializers.IntegerField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['sid'] = int(user.sid)
        token['name'] = user.name
        # ★ [추천] 토큰 안에도 role 정보를 넣어두면 프론트엔드에서 편합니다.
        token['role'] = user.role 
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['sid'] = self.user.sid
        data['name'] = self.user.name
        data['email'] = self.user.email
        # ★ [추천] 로그인 결과에도 role 정보를 포함시킵니다.
        data['role'] = self.user.role 
        
        return data