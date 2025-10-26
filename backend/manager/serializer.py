from rest_framework import serializers
from .models import Manager
from members.serializer import MemberSerializer

class ManagerSerializer(serializers.ModelSerializer):
    manager_sid = MemberSerializer(read_only=True) # ForeignKey 관계의 Member 정보를 중첩 직렬화
    class Meta:
        model = Manager
        fields = ['manager_sid', 'manager_type', 'manager_last_activity']
        