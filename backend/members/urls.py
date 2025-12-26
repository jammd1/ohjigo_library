from django.urls import path
from .views import MemberViewSet, CustomTokenObtainPairView
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', '', '1234')
        return HttpResponse("계정 생성 성공! 아이디: admin / 비번: 1234")
    return HttpResponse("이미 계정이 있습니다.")

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', MemberViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='member-list'),
    path('<int:sid>/', MemberViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='member-detail'),
]