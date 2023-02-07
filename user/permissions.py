from rest_framework.permissions import BasePermission


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'support')


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'customer')
