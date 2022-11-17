import datetime

from apiart.models import Category, Genre, Title, Review, Comment
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


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
    year = serializers.IntegerField(min_value=1000, max_value=2022, required=True)
    class Meta:
        fields = ('id', 'name', 'genre', 'category', 'description', 'year')
        model = Title


    def validate_year(self, value):
        """Валидатор на указание произведения (год выпуска не может быть больше текущего)."""
        now = datetime.date.today().year
        if value >= now:
            raise serializers.ValidationError('Нельзя добавлять произведения, которые еще не вышли ')
        return value
    pass


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user, title__id=self.context[
                'request'].parser_context['kwargs']['title_id']).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
