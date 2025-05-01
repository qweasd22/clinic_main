from rest_framework import serializers
from clinic.models import Doctor, Patient, Visit, Service

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'