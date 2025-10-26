from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSet

# 라우터 설정
router = DefaultRouter()
router.register('managers', ManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]