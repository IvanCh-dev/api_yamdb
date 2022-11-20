from api.validators import ValidationUser
from rest_framework import serializers
from users.models import User


class SignupSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация auth/sighup.'''
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class GettingTokenSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация get_token.'''
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных User.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
