from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Permiso que permite acceso solo a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
