from rest_framework import serializers
from .models import Book
from .models import Loan
from .models import Notice


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # 모든 필드 직렬화

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__' # 모든 필드 직렬화

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__' # 모든 필드 직렬화