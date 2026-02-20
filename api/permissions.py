from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'recruiter'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'