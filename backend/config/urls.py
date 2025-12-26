from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from members.views import CustomTokenObtainPairView
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    User.objects.create_superuser('admin', '', '1234') if not User.objects.filter(username='admin').exists() else None
    return HttpResponse("Admin OK")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("library/", include("library.urls")),
    path("manager/", include("manager.urls")),
    path("api/", include("library.urls")),
    path("api/members/", include("members.urls")),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]