import datetime

from rest_framework import serializers

from apiart.models import (Category, Comment,
                           Genre, Review, Title)


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


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для get запроса  списка произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')


class TitlePostSerializer(serializers.ModelSerializer):
    """Серилизатор для добавления (запрос Post ) произвдения -
    приявязываетяся адрес жанра/категории с name.
    """

    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True
                                         )
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug'
                                            )
    year = serializers.IntegerField(max_value=2022, min_value=1000)

    class Meta:
        fields = ('name', 'genre', 'category', 'description', 'year')
        model = Title

    def to_representation(self, instance):
        return TitleGetSerializer(instance).data

    def validate_year(self, value):
        """Валидатор на указание произведения
        (год выпуска не может быть больше текущего).
        """
        now = datetime.date.today().year
        if value >= now:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        """Валидатор сначала передаём запрос далее , определяем тип запроса
        и если запрос пост и юзер УЖЕ отправил отзыв, то рейзанётся ошибка
        """
        request = self.context['request']
        if Review.objects.filter(
            author=self.context['request'].user, title__id=self.context[
                'request'].parser_context['kwargs']['title_id']).exists() and request.method == "POST":
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
