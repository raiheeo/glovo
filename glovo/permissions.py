from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, 'status', None) == 'admin' and
            request.user.is_staff
        )


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'status', None) == 'client'


class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'status', None) == 'courier'


class IsOwnProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'status', None) == 'owner'


class CheckOwnerEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class CheckAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.status.lower() == 'client':
            return True
