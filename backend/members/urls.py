from django.urls import path
from .views import MemberViewSet, RegistrationView

# The router is no longer used for MemberViewSet
# We define the URLs manually to enforce integer type for sid

urlpatterns = [
    # Map viewset actions to URLs manually
    path('members/', MemberViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='member-list'),
    path('members/<int:sid>/', MemberViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='member-detail'),

    # The registration view remains the same
    path('register/', RegistrationView.as_view(), name='register'),
]
