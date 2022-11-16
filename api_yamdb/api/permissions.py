from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ есть только у администратора.'

    def has_permission(self, request, view):
        return (request.user.uthenticated
                and request.user.admin or request.user.superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    message = ('Доступ есть только у администратора')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.admin or request.user.superuser))


class AuthorAndStaffOrReadOnly(permissions.BasePermission):
    message = ('Доступ есть только у администратора, модератора и автора!')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.authenticated:
            return False
        return (obj.author == request.user
                or request.user.admin
                or request.user.moderator)
