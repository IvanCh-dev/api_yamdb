from apiart.filters import CustomTitleFilter
from apiart.models import Category, Genre, Title, Review
from apiart.serializers import (CategorySerializer, GenreSerializer,
                                TitleGetSerializer, TitlePostSerializer,
                                ReviewSerializer, CommentSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
# from api.permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """Предсттавление Категории (типы) произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    # permission_classes = [IsAdminOrReadOnly,]
    """настроена пагинация"""
    pagination_class = PageNumberPagination
    """Поиск по названию категории"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию категории"""
    search_fields = ('name',),
    """переход на определенный жанр(id категории) через slug"""
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Представление Категории жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    # permission_classes =  [IsAdminOrReadOnly,]
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    """Поиск по названию жанра"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию жанра"""
    search_fields = ('name',),
    """переход на определенный жанр(id жанра) через slug"""
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление апи через вьюсеты для работы с произведениями"""
    queryset = Title.objects.all()
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [DjangoFilterBackend, ]
    """
    фильтрует по полю slug категории,
    фильтрует по полю slug жанра,
    фильтрует по названию произведения,
    фильтрует по году
    """
    filterest_class = CustomTitleFilter
    """настроена пагинации"""
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list'):
            return TitleGetSerializer
        return TitlePostSerializer


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')).comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
