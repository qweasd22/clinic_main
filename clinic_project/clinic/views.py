from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Service, Visit, Patient
from .forms import PatientSignUpForm, AppointmentForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    featured_services = Service.objects.all()[:3]
    featured_doctors = Doctor.objects.filter(category__gte=2)[:2]  # Фильтр по категории
    return render(request, 'clinic/home.html', {
        'featured_services': featured_services,
        'featured_doctors': featured_doctors  # Убедитесь, что переменная передается
    })

@login_required
def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctors_list.html', {'doctors': doctors})

@login_required
def services_list(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})

@login_required
def visits_list(request):
    visits = Visit.objects.all().prefetch_related(
        'services__service',
        'services__doctor',
        'patient__user'
    )
    
    if not request.user.groups.filter(name='Admin').exists():
        visits = visits.filter(patient=request.user.patient)
    
    return render(request, 'clinic/visits.html', {'visits': visits})

@login_required
def profile(request):
    patient = (getattr(request.user, 'patient', None))
    latest_visits = Visit.objects.filter(patient=patient).order_by('-date')[:3]
    return render(request, 'clinic/profile.html', {
        'patient': patient,
        'latest_visits': latest_visits
    })


def signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientSignUpForm()
    return render(request, 'clinic/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            
            return redirect('visits')
    else:
        form = AppointmentForm()
    
    return render(request, 'clinic/create_appointment.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'clinic/login.html'
    redirect_authenticated_user = True 

def services_list(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})