from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient, Doctor, Service, Visit, ServiceRecord

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Service)
admin.site.register(Visit)
admin.site.register(ServiceRecord)