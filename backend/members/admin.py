from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('sid', 'name', 'email', 'role', 'status', 'is_staff')
    list_display_links = ('sid', 'name')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    search_fields = ('sid', 'name', 'email')
    ordering = ('sid',)
    fieldsets = (
        ('기본 정보', {'fields': ('sid', 'password')}),
        ('개인 정보', {'fields': ('name', 'email', 'role', 'status')}),
        ('권한 설정', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')