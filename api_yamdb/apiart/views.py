
from api.permissions import IsAdminOrReadOnly
from apiart.filters import CustomTitleFilter
from apiart.models import Category, Genre, Title
from apiart.serializers import (CategorySerializer, GenreSerializer,
                                TitleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """Предсттавление Категории (типы) произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    permission_classes = [IsAdminOrReadOnly,]
    """настроена пагинация"""
    pagination_class = PageNumberPagination
    """Поиск по названию категории"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию категории"""
    search_fields = ('=category__slug',)

    
class GenreViewSet(viewsets.ModelViewSet):
    """Представление Категории жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    permission_classes =  [IsAdminOrReadOnly,]
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    """Поиск по названию жанра"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию жанра"""
    search_fields = ('=genre__slug',)

class TitleViewSet(viewsets.ModelViewSet):
    """Представление апи через вьюсеты для работы с произведениями"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [DjangoFilterBackend,]
    """
    фильтрует по полю slug категории,
    фильтрует по полю slug жанра,
    фильтрует по названию произведения,
    фильтрует по году
    """
    filterest_class = CustomTitleFilter
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    