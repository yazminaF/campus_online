from rest_framework.permissions import BasePermission

class IsOwnerPerfil(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user
