from rest_framework import viewsets, permissions
from clinic.models import Doctor, Patient, Visit, Service,User
from .serializers import DoctorSerializer, PatientSerializer, VisitSerializer, ServiceSerializer, UserSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAdminUser]

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAdminUser]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]
    
    # Дополнительные настройки при необходимости
    filterset_fields = ['specialty']
    search_fields = ['name']
    ordering_fields = ['base_cost']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
