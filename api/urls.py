from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('doctors/', views.doctors_list, name='doctors'),
    path('doctors/<int:pk>/status/', views.doctor_status, name='doctor_status'),
    path('departments/', views.departments_view, name='departments'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/<int:pk>/status/', views.appointment_status, name='appointment_status'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
]
