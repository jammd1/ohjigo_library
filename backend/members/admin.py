from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # 1. 목록에서 보여줄 필드 (학번, 이름, 이메일, 신분, 상태 등)
    list_display = ('sid', 'name', 'email', 'role', 'status', 'is_staff')
    
    # 2. 클릭해서 상세 정보로 들어갈 수 있는 필드
    list_display_links = ('sid', 'name')
    
    # 3. 우측 필터 바 (신분이나 계정 상태별로 모아보기 편함)
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    
    # 4. 검색 기능 (학번이나 이름으로 바로 찾기)
    search_fields = ('sid', 'name', 'email')
    
    # 5. 정렬 기준 (학번 순)
    ordering = ('sid',)

    # 6. 상세 수정 화면 레이아웃
    fieldsets = (
        ('기본 정보', {'fields': ('sid', 'password')}),
        ('개인 정보', {'fields': ('name', 'email', 'role', 'status')}),
        ('권한 설정', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    
    # 비밀번호 수정을 안전하게 하기 위한 설정 (선택 사항)
    readonly_fields = ('last_login', 'date_joined')