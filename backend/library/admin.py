from django.contrib import admin
from .models import Book, Loan, Notice

# 1. 도서 관리 (검색 & 필터 추가)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 목록에 보여줄 항목들
    list_display = ('book_id', 'call_number', 'title', 'author', 'status', 'location')
    
    # 검색창 (제목, 저자, 청구기호로 검색 가능)
    search_fields = ('title', 'author', 'call_number')
    
    # 우측 필터 (상태별, 언어별, 분야별 보기)
    list_filter = ('status', 'language', 'category')


# 2. 대출 관리 (여기가 제일 중요! 자동 계산된 날짜 확인용)
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    # 목록에 보여줄 항목들 (회원정보와 연체여부 포함)
    list_display = ('loan_id', 'get_book_title', 'get_member_info', 'loan_date', 'due_date', 'return_date', 'is_overdue')
    
    # 검색창 (책 제목, 회원 이름, 학번으로 검색)
    search_fields = ('book__title', 'member__name', 'member__sid')
    
    # 우측 필터 (대출일, 반납여부)
    list_filter = ('loan_date', 'return_date')

    # ★ 수정 페이지에서 날짜는 자동 계산되므로 '읽기 전용'으로 보여줌 (실수 방지)
    readonly_fields = ('due_date', 'loan_date')

    # [보조 함수] 책 제목 표시
    def get_book_title(self, obj):
        return obj.book.title
    get_book_title.short_description = "도서명"

    # [보조 함수] 회원 이름 + 신분 표시
    def get_member_info(self, obj):
        return f"{obj.member.name} ({obj.member.get_role_display()})"
    get_member_info.short_description = "회원(신분)"

    # [보조 함수] 연체 여부 O/X 아이콘으로 표시
    def is_overdue(self, obj):
        return obj.overdue_days > 0
    is_overdue.boolean = True # 아이콘 활성화
    is_overdue.short_description = "연체"


# 3. 공지사항 관리
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('notice_id', 'title', 'manager', 'post_date', 'view_count')
    search_fields = ('title', 'content')