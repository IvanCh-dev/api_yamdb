
from apiart.models import Category, Genre, Title
from apiart.searches import CustomApiFilter
from apiart.serializers import TitleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Представление апи через вьюсеты для работы с произведениями"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer 
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = CustomApiFilter # настроен фильтр 
    pagination_class = PageNumberPagination # настроена пагинация