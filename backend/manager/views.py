# Create your views here.
from rest_framework import viewsets, permissions
from .models import Manager
from .serializer import ManagerSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.select_related('manager_sid').all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAdminUser]