from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель для работы с категориями произведений"""
    name = models.CharField(max_length=256,
                            verbose_name='Категория'
                            )
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес')

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для работы с жанрами произведений"""
    name = models.CharField(max_length=256,
                            verbose_name='Жанр'
                            )
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес')

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(max_length=255,
                            verbose_name='Название произведения')
    """Одно произведение может быть привязано к нескольким жанрам."""
    genre = models.ManyToManyField(Genre,
                                   through='TitleGenre',
                                   through_fields=('title', 'genre'),
                                   verbose_name='Жанр произведения'
                                   )
    description = models.TextField(max_length=255,
                                   verbose_name='Описание произведения',
                                   null=True,
                                   blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Название Категории'
    )
    year = models.PositiveIntegerField(
        validators=(MaxValueValidator(
                    datetime.now().year,
                    message=(
                        'Нельзя добавлять произведения,которые еще не вышли')
                    ),
                    ),
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitles',
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
