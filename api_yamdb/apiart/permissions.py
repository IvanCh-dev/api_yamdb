"""есть пермишены только пока на авторизирвоанного во вью закомитила пока пермишены """

from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
pass