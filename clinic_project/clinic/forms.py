from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient

class PatientSignUpForm(UserCreationForm):
    middle_name = forms.CharField(max_length=100)
    birth_year = forms.IntegerField()
    discount_category = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        Patient.objects.create(
            user=user,
            middle_name=self.cleaned_data['middle_name'],
            birth_year=self.cleaned_data['birth_year'],
            discount_category=self.cleaned_data['discount_category']
        )
        return user
    
from django import forms
from django.utils import timezone
from .models import Visit

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['doctor', 'service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        doctor = cleaned_data.get('doctor')
        
        if date < timezone.now().date():
            raise forms.ValidationError("Нельзя записаться на прошедшую дату")
            
        if Visit.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise forms.ValidationError("Это время уже занято")
            
        return cleaned_data
    
    
