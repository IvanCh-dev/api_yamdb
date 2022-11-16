from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AdminOrReadonly(permissions.BasePermission):
    """
    Права доступа:
    чтение для всех
    изменение только для администраторa
    """