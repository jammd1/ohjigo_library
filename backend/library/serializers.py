from rest_framework import serializers
from .models import Book, Loan, Notice

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    book_author = serializers.ReadOnlyField(source='book.author')

    class Meta:
        model = Loan
        fields = [
            'loan_id', 
            'member', 
            'book', 
            'book_title',   
            'book_author',  
            'loan_date', 
            'due_date', 
            'return_date', 
            'overdue_days'
        ]

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'