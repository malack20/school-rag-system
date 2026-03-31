from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not isinstance(request.user, User):
            return False
        return request.user.is_staff
