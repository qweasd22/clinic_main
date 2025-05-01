from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
]