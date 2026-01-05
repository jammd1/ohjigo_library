from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Book, Loan, Notice

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = (
            'call_number', 'title', 'author', 'status', 
            'language', 'location', 'category'
        )
        import_id_fields = ('call_number',)

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin): 
    resource_class = BookResource 
    list_display = ('book_id', 'call_number', 'title', 'author', 'status', 'location')
    search_fields = ('title', 'author', 'call_number')
    list_filter = ('status', 'language', 'category')

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

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('notice_id', 'title', 'manager', 'post_date', 'view_count')
    search_fields = ('title', 'content')