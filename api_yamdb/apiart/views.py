from apiart.filters import CustomTitleFilter
from apiart.models import Category, Genre, Title
#from apiart.permissions import OwnerOrReadOnly
from apiart.serializers import (CategorySerializer, GenreSerializer,
                                TitleSerializer, ReviewSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import IsAdminOrReadOnly


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet
                      ):
    """Предсттавление Категории (типы) произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    #permission_classes = [IsAdminOrReadOnly,]
    """настроена пагинация"""
    pagination_class = PageNumberPagination
    """переход на категорию по слагу"""
    lookup_field = 'slug'
    """Поиск по названию категории"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по имени произведения"""
    search_fields = ('=name',)


class GenreViewSet(
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                    ):
    """Представление Категории жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    #permission_classes =  (IsAdminOrReadOnly,)
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    """Поиск по названию жанра"""
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    """Поиск по названию жанра"""
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление апи через вьюсеты для работы с произведениями"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    """Права разрешения: если админ то есть все права, если не админ то только SAFE_METHODS доступ на прочтение"""
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend,]
    """переход по страницам {titles_id}"""
    lookup_field='id'
    """
    фильтрует по полю slug категории,
    фильтрует по полю slug жанра,
    фильтрует по названию произведения,
    фильтрует по году
    """
    lookup_field = 'id'
    search_fields = ('=name',)
    filterest_class = CustomTitleFilter
    """настроена пагинации"""
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = get_object_or_404(
            Title, id=self.kwargs.get('title_id')).reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
