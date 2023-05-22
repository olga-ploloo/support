from rest_framework.permissions import BasePermission

from backend.user.models import User


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.Role.SUPPORT)


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.Role.CUSTOMER)
