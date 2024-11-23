from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManager(BasePermission):
    """
    Permite el acceso a usuarios con rol 'manager' y 'admin' (pero no 'accountant').
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']

class IsAccountant(BasePermission):
    """
    Permite el acceso a usuarios con rol 'accountant' y 'admin' (pero no 'manager').
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'accountant']
