# members/urls.py

from django.urls import path
from .views import MemberViewSet # RegistrationView는 이제 사용 안 함

urlpatterns = [
    # 4. (핵심) 'members/' -> '' (빈 문자열)로 변경
    # /api/members/ (GET, POST) 요청을 처리
    path('', MemberViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='member-list'),
    
    # /api/members/<int:sid>/ 요청을 처리
    path('<int:sid>/', MemberViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='member-detail'),
]