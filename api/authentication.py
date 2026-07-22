import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from .models import Patient, Doctor, Admin

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        user_id = payload.get('user_id')
        role = payload.get('role')

        if not user_id or not role:
            raise exceptions.AuthenticationFailed('Invalid payload')

        if role == 'patient':
            try:
                user = Patient.objects.get(patient_id=user_id)
            except Patient.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
        elif role == 'doctor':
            try:
                user = Doctor.objects.get(doctor_id=user_id)
            except Doctor.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
        elif role == 'admin':
            try:
                user = Admin.objects.get(admin_id=user_id)
            except Admin.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
        else:
            raise exceptions.AuthenticationFailed('Invalid role')

        user.role = role
        user.is_authenticated = True
        return (user, token)
