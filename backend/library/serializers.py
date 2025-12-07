from rest_framework import serializers
from .models import Book, Loan, Notice

# 1. 도서 시리얼라이저
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# 2. 대출 시리얼라이저 (아까 고친 책 제목 나오는 버전)
class LoanSerializer(serializers.ModelSerializer):
    # 책 제목과 저자를 가져오는 마법의 코드
    book_title = serializers.ReadOnlyField(source='book.title')
    book_author = serializers.ReadOnlyField(source='book.author')

    class Meta:
        model = Loan
        fields = [
            'loan_id', 
            'member', 
            'book', 
            'book_title',   # ★ 책 제목
            'book_author',  # ★ 책 저자
            'loan_date', 
            'due_date', 
            'return_date', 
            'overdue_days'
        ]

# 3. ★ [복구 완료] 공지사항 시리얼라이저 (이게 없어서 에러 남)
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'