import datetime

from apiart.models import Category, Genre, Title
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """серилиазтор для категории"""
    class Meta:
        fields = ('name', 'slug')
        model = Category

class GenreSerializer(serializers.ModelSerializer):
    """серилиазтор для жанров"""
    class Meta:
        fields = ('name', 'slug')
        model = Genre

class TitleSerializer(serializers.ModelSerializer):
    """серилиазтор для названия/произведения"""
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True
                                        )
    category = serializers.SlugRelatedField(
                                            queryset=Category.objects.all(),
                                            slug_field='slug'
                                            )
    year = serializers.IntegerField(max_value=2020, min_value=1000)
    class Meta:
        fields = ('name', 'genre', 'category', 'description', 'year')
        model = Title
    def validate_year(self, value):
        """Валидатор на указание произведения (год выпуска не может быть больше текущего)."""
        now = datetime.date.today().year
        if value >= now:
            raise serializers.ValidationError('Нельзя добавлять произведения, которые еще не вышли ')
        return value
    pass