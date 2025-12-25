from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Book, Loan, Notice

# --- 0. Book용 Import-Export 리소스 설정 ---
class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        # CSV에서 가져올 필드 정의 (필드 순서는 상관없음)
        fields = (
            'call_number', 'title', 'author', 'status', 
            'language', 'location', 'category'
        )
        # 청구기호(call_number)를 기준으로 중복 체크 및 업데이트
        import_id_fields = ('call_number',)

# 1. 도서 관리 (ImportExportModelAdmin 적용)
@admin.register(Book)
class BookAdmin(ImportExportModelAdmin): # 클래스 상속 변경
    resource_class = BookResource # 리소스 연결
    
    # 기존에 사용하시던 설정 그대로 유지
    list_display = ('book_id', 'call_number', 'title', 'author', 'status', 'location')
    search_fields = ('title', 'author', 'call_number')
    list_filter = ('status', 'language', 'category')


# 2. 대출 관리 (기존 코드 유지)
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'get_book_title', 'get_member_info', 'loan_date', 'due_date', 'return_date', 'is_overdue')
    search_fields = ('book__title', 'member__name', 'member__sid')
    list_filter = ('loan_date', 'return_date')
    readonly_fields = ('due_date', 'loan_date')

    def get_book_title(self, obj):
        return obj.book.title
    get_book_title.short_description = "도서명"

    def get_member_info(self, obj):
        return f"{obj.member.name} ({obj.member.get_role_display()})"
    get_member_info.short_description = "회원(신분)"

    def is_overdue(self, obj):
        return obj.overdue_days > 0
    is_overdue.boolean = True
    is_overdue.short_description = "연체"


# 3. 공지사항 관리 (기존 코드 유지)
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('notice_id', 'title', 'manager', 'post_date', 'view_count')
    search_fields = ('title', 'content')