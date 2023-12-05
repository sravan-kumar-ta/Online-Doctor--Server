from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        # Check if the user's role is 'doctor'
        return request.user.role == 'doctor'
