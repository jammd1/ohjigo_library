from django.contrib import admin
from .models import Manager

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    # 1. 목록 화면에서 보여줄 열 설정
    list_display = ('manager_sid', 'manager_type', 'join_date')
    
    # 2. [가장 중요] UI에서 멤버를 선택할 때 '학번(sid)'을 직접 입력하거나 
    # 팝업창으로 선택하게 하여 IntegrityError를 방지합니다.
    raw_id_fields = ('manager_sid',)
    
    # 3. 관리자 유형으로 필터링해서 보기 가능
    list_filter = ('manager_type',)
    
    # 4. 검색창 추가 (학번이나 이름으로 관리자 검색 가능)
    search_fields = ('manager_sid__sid', 'manager_sid__name')

    # 관리자 등록 화면을 좀 더 깔끔하게 보기 위한 설정
    fields = ('manager_sid', 'manager_type', 'manager_last_activity')
    readonly_fields = ('manager_last_activity',)