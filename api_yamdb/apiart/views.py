from api.permissions import IsAdminOrReadOnly, IsModeratorOrAdminOrAuthor
from apiart.filters import CustomTitleFilter
from apiart.models import Category, Genre, Review, Title
from apiart.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                TitleGetSerializer, TitlePostSerializer)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Предсттавление Категории (типы) произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    permission_classes = (IsAdminOrReadOnly, )
    """настроена пагинация"""
    pagination_class = PageNumberPagination
    """Поиск по названию категории"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию категории"""
    search_fields = ('=name',)
    """переход на определенный жанр(id категории) через slug"""
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Представление Категории жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    permission_classes = (IsAdminOrReadOnly, )
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    """Поиск по названию жанра"""
    filter_backends = (filters.SearchFilter,)
    """Поиск по названию жанра"""
    search_fields = ('=name',)
    """переход на определенный жанр(id жанра) через slug"""
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление апи через вьюсеты для работы с произведениями"""
    """Права разрешения: если админ то есть все права, если не админ
    то только SAFE_METHODS доступ на прочтение.
    """
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    """
    фильтрует по полю slug категории,
    фильтрует по полю slug жанра,
    фильтрует по названию произведения,
    фильтрует по году
    """
    filterest_class = CustomTitleFilter
    """настроена пагинации"""
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        if self.action in ('list'):
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        queryset = Title.objects.annotate(rating=Avg('reviews__score'))
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAdminOrAuthor, )
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
    permission_classes = (IsModeratorOrAdminOrAuthor, )
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
