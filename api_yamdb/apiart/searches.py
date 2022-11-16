from django_filters import rest_framework

from .models import Title


class CustomApiFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = rest_framework.CharFilter(field_name='genre__slug', lookup_expr='exact')
    name = rest_framework.CharFilter(field_name='name', lookup_expr='icontains')
    name = rest_framework.CharFilter(field_name='year', lookup_expr='icontains')
    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
