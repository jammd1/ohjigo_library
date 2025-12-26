from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['sid', 'name', 'email', 'status', 'join_date', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Member.USERNAME_FIELD 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        if 'username' in self.initial_data:
            self.initial_data[self.username_field] = self.initial_data.pop('username')[0] if isinstance(self.initial_data.get('username'), list) else self.initial_data.get('username')

    def validate(self, attrs):
        data = super().validate(attrs)
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
        user = Member.objects.create_user(
            sid=validated_data['sid'],
            username=str(validated_data['sid']), 
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'UNDERGRADUATE')
        )
        return user