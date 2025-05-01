from rest_framework import serializers
from clinic.models import Doctor, Patient, Visit, Service, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {
            'photo': {'required': False}
        }

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('discounted_price',)  # Если есть вычисляемые поля