from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal 
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Schedule(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField("Дата приёма")
    start_time = models.TimeField("Начало работы")
    end_time = models.TimeField("Окончание работы")
class Doctor(models.Model):
    CATEGORY_CHOICES = [
        (1, 'Вторая категория'),
        (2, 'Первая категория'),
        (3, 'Высшая категория'),
    ]

    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    specialty = models.CharField("Специальность", max_length=100)
    category = models.IntegerField("Категория", choices=CATEGORY_CHOICES)
    photo = models.ImageField("Фото", upload_to='doctors/', blank=True, null=True)
    experience = models.PositiveIntegerField("Стаж работы", default=0)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField("Отчество", max_length=100)
    birth_year = models.IntegerField("Год рождения")
    discount_category = models.CharField("Категория скидки", max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200)
    base_cost = models.DecimalField("Базовая стоимость", max_digits=10, decimal_places=2)
    specialty = models.CharField("Специальность", max_length=100)

    @property
    def discounted_price(self):
        # Пример расчета скидки 10% 
        return self.base_cost * Decimal('0.9')
    def __str__(self):
        return self.name

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField("Дата приема")
    time = models.TimeField("Время приема")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает подтверждения'),
            ('confirmed', 'Подтвержден'),
            ('completed', 'Завершен'),
            ('canceled', 'Отменен')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_cost(self):
        return self.services.aggregate(total=Sum('cost'))['total'] or 0

    def __str__(self):
        return f"Обращение #{self.id} от {self.date}"

class ServiceRecord(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Применение скидки 10% при наличии категории
        discount_multiplier = Decimal('0.9') if self.visit.patient.discount_category else Decimal('1')
        self.cost = self.service.base_cost * discount_multiplier
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} ({self.cost} руб.)"