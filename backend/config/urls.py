# config/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from members.views import CustomTokenObtainPairView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("library/", include("library.urls")),
    path("manager/", include("manager.urls")),
    path("api/books/", include("library.urls")),
    # ... (다른 앱들) ...

    # 3. (핵심) 'members/'가 아니라 'api/members/' 입니다.
    path("api/members/", include("members.urls")),

    # ... (drf-spectacular, simplejwt 등) ...
    # 'api/token/' 경로는 이미 잘 되어 있습니다.
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]