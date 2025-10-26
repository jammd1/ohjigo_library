from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, RegistrationView

# 라우터 설정
router = DefaultRouter()
router.register('members', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),
]