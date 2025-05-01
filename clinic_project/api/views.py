from rest_framework import viewsets, permissions
from clinic.models import Doctor, Patient, Visit
from .serializers import DoctorSerializer, PatientSerializer, VisitSerializer

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