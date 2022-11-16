from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин',
    )
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True,
        verbose_name='Почтовый адрес'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.TextField(
        blank=True,
        choices=ROLES,
        default='user',
        verbose_name='Текущая роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""
        return self.username
