from rest_framework.permissions import BasePermission

class IsAdminPermission(BasePermission):
    """
    Custom permission to grant access to sellers only.
    """

    def has_permission(self, request, view):
       
        # Check if the user is a seller (based on the is_seller field).
        return request.user.is_authenticated and request.user.is_superuser