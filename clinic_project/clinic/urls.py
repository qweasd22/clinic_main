from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('services/', views.services_list, name='services'),
    path('visits/', views.visits_list, name='visits'),
    path('profile/', views.profile, name='profile'),
    
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]