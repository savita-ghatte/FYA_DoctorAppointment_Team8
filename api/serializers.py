from rest_framework import serializers
from .models import Patient, Doctor, Admin, Department, Appointment, Prescription, Review, Notification

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'age', 'gender', 'email', 'phone', 'address']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

from django.db.models import Avg
class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    rating = serializers.SerializerMethodField()
    patient_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['doctor_id', 'department', 'department_name', 'name', 'qualification', 'specialization', 'experience', 'hospital', 'fees', 'available_days', 'available_time', 'email', 'phone', 'rating', 'review_count', 'status', 'patient_count']
        

    def get_patient_count(self, obj):
        return Appointment.objects.filter(doctor=obj).values('patient_id').distinct().count()

    def get_rating(self, obj):
        avg = Review.objects.filter(doctor=obj).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    def get_review_count(self, obj):
        return Review.objects.filter(doctor=obj).count()

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['admin_id', 'username', 'email']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    department_name = serializers.CharField(source='doctor.department.department_name', read_only=True)
    hospital = serializers.CharField(source='doctor.hospital', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
