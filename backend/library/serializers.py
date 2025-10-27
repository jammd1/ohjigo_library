from rest_framework import serializers
from .models import Book, Loan, Notice

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'book_id', 
            'call_number', 
            'title', 
            'author', 
            'status', 
            'registrar_manager', 
            'registration_date', 
            'modification_manager', 
            'modification_date'
        ]

class LoanSerializer(serializers.ModelSerializer):
    # overdue_days는 모델의 프로퍼티이므로 읽기 전용 필드로 추가합니다.
    overdue_days = serializers.ReadOnlyField()

    class Meta:
        model = Loan
        fields = [
            'loan_id', 
            'member', 
            'book', 
            'loan_date', 
            'due_date', 
            'return_date', 
            'loan_manager',
            'overdue_days'
        ]

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'notice_id', 
            'manager', 
            'title', 
            'content', 
            'post_date', 
            'view_count'
        ]
