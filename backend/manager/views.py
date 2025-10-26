# Create your views here.
from rest_framework import viewsets
from .models import Manager
from .serializer import ManagerSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.select_related('manager_sid').all()
    serializer_class = ManagerSerializer