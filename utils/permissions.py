from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            (request.user.is_authenticated and request.user.is_active))


class IsPartiallyAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class UserPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
