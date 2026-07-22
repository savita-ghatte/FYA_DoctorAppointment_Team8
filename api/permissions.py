from rest_framework import permissions

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', None) == 'patient')

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', None) == 'doctor')

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', None) == 'admin')
