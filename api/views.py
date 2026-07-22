import jwt
import datetime
from django.db.models import Avg
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Doctor, Admin, Department, Appointment, Review, Notification
from .serializers import PatientSerializer, DoctorSerializer, AdminSerializer, DepartmentSerializer, AppointmentSerializer
from .permissions import IsPatient, IsDoctor, IsAdminUser
from rest_framework.permissions import IsAuthenticated

def generate_jwt(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'patient')

    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    if role == 'patient':
        user = Patient.objects.filter(email=email, password=password).first()
        user_id = user.patient_id if user else None
    elif role == 'doctor':
        user = Doctor.objects.filter(email=email, password=password).first()
        user_id = user.doctor_id if user else None
    elif role == 'admin':
        user = Admin.objects.filter(email=email, password=password).first()
        user_id = user.admin_id if user else None
    else:
        return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token = generate_jwt(user_id, role)
    return Response({'token': token, 'role': role, 'user_id': user_id})

@api_view(['POST'])
def register_view(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'patient')

    if role == 'patient':
        if Patient.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        user = Patient.objects.create(name=name, email=email, password=password)
        token = generate_jwt(user.patient_id, 'patient')
        return Response({'token': token, 'role': 'patient', 'user_id': user.patient_id})

    elif role == 'doctor':
        if Doctor.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        user = Doctor.objects.create(name=name, email=email, password=password)
        token = generate_jwt(user.doctor_id, 'doctor')
        return Response({'token': token, 'role': 'doctor', 'user_id': user.doctor_id})

    elif role == 'admin':
        if Admin.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        username = email.split('@')[0]
        if Admin.objects.filter(username=username).exists():
            import random
            username = f"{username}{random.randint(100, 999)}"
        user = Admin.objects.create(username=username, email=email, password=password)
        token = generate_jwt(user.admin_id, 'admin')
        return Response({'token': token, 'role': 'admin', 'user_id': user.admin_id})
    else:
        return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    role = request.user.role
    if request.method == 'GET':
        if role == 'patient':
            serializer = PatientSerializer(request.user)
        elif role == 'doctor':
            serializer = DoctorSerializer(request.user)
        else:
            serializer = AdminSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Update logic here
        return Response({'message': 'Profile updated'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctors_list(request):
    doctors = Doctor.objects.all()
    search = request.query_params.get('search')
    dept = request.query_params.get('department')
    if search:
        doctors = doctors.filter(name__icontains=search)
    if dept and dept != 'Specialization' and dept != 'All':
        doctors = doctors.filter(department__department_name__icontains=dept)
    
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointments_view(request):
    if request.method == 'POST':
        if request.user.role != 'patient':
            return Response({'error': 'Only patients can book'}, status=status.HTTP_403_FORBIDDEN)
        
        doctor_id = request.data.get('doctor_id')
        date = request.data.get('date')
        time = request.data.get('time')
        reason = request.data.get('reason', '')
        
        appt = Appointment.objects.create(
            patient=request.user,
            doctor_id=doctor_id,
            appointment_date=date,
            appointment_time=time,
            reason=reason,
            status='Pending'
        )
        return Response(AppointmentSerializer(appt).data, status=status.HTTP_201_CREATED)
    
    # GET
    if request.user.role == 'patient':
        appts = Appointment.objects.filter(patient=request.user).order_by('appointment_date', 'appointment_time')
    elif request.user.role == 'doctor':
        appts = Appointment.objects.filter(doctor=request.user).order_by('appointment_date', 'appointment_time')
    else:
        appts = Appointment.objects.all().order_by('-appointment_id')
        
    serializer = AppointmentSerializer(appts, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def appointment_status(request, pk):
    try:
        appt = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    new_status = request.data.get('status')
    if new_status in dict(Appointment.STATUS_CHOICES):
        appt.status = new_status
        appt.save()
        return Response(AppointmentSerializer(appt).data)
    return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    role = request.user.role
    stats = {}
    today = datetime.date.today()
    if role == 'patient':
        appts = Appointment.objects.filter(patient=request.user)
        stats['upcoming'] = appts.filter(status='Approved', appointment_date__gte=today).count()
        stats['pending'] = appts.filter(status='Pending').count()
        stats['completed'] = appts.filter(status='Completed').count()
        stats['doctors_seen'] = appts.filter(status='Completed').values('doctor_id').distinct().count()
        
        # Next appointment string
        next_appt = appts.filter(status='Approved', appointment_date__gte=today).order_by('appointment_date', 'appointment_time').first()
        if next_appt:
            if next_appt.appointment_date == today:
                stats['next_appt_str'] = f"Today {next_appt.appointment_time}"
            else:
                stats['next_appt_str'] = f"{next_appt.appointment_date.strftime('%b %d')} {next_appt.appointment_time}"
        else:
            stats['next_appt_str'] = "No upcoming appointments"
            
    elif role == 'doctor':
        appts = Appointment.objects.filter(doctor=request.user)
        stats['today_appts'] = appts.filter(appointment_date=today).count()
        stats['total_patients'] = appts.values('patient_id').distinct().count()
        stats['pending_approvals'] = appts.filter(status='Pending').count()
        stats['rating'] = 4.8
        
    elif role == 'admin':
        stats['today_appts'] = Appointment.objects.filter(appointment_date=today).count()
        stats['total_doctors'] = Doctor.objects.count()
        stats['total_patients'] = Patient.objects.count()
        stats['total_appointments'] = Appointment.objects.count()
        stats['pending_approvals'] = Appointment.objects.filter(status='Pending').count()
        
        # 7-day chart data
        chart_data = []
        for i in range(6, -1, -1):
            d = today - datetime.timedelta(days=i)
            c = Appointment.objects.filter(appointment_date=d).count()
            chart_data.append(c)
        stats['chart_data'] = chart_data
        
    # Notifications
    stats['notifications'] = Notification.objects.filter(user_type=role.capitalize(), user_id=user_id, is_read=False).count()
    return Response(stats)

@api_view(['GET'])
def departments_view(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def doctor_status(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    new_status = request.data.get('status')
    if new_status in ['Active', 'Suspended']:
        doctor.status = new_status
        doctor.save()
        return Response({'message': 'Status updated'})
    return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
