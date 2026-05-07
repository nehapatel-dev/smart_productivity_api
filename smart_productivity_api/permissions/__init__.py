from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """Object-level permission: only the owner can access/modify."""
    message = "You can only access your own resources."

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id
