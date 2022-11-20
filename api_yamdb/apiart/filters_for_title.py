from apiart.models import Title
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter


class CustomTitleFilter(FilterSet):
    """
    фильтрует по полю slug категории (category),
    фильтрует по полю slug жанра(genre),
    фильтрует по названию произведения(name),
    фильтрует по году(year)
    """
    year = NumberFilter(field_name='year',)
    category = CharFilter(field_name='=category__slug',)
    genre = CharFilter(field_name='=genre__slug',)
    name = CharFilter(field_name='=name',)

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
