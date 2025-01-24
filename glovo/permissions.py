from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'admin'

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'client'

class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'courier'

class IsOwnProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.status == 'owner'

class CheckOwnerEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

class CheckAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.status == 'Client':
            return True
        return False