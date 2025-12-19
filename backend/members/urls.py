# members/urls.py

from django.urls import path
from .views import MemberViewSet # RegistrationView는 이제 사용 안 함
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        # 아이디: admin, 이메일: 없음, 비밀번호: 1234로 생성
        User.objects.create_superuser('admin', '', '1234')
        return HttpResponse("계정 생성 성공! 아이디: admin / 비번: 1234")
    return HttpResponse("이미 계정이 있습니다.")

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