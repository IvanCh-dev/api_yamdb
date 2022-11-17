from api.validators import UserDataValidation
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer, UserDataValidation):
    '''Сериализация данных .'''
    class Meta:
        model = User
        fields = ('last_name', 'bio', 'role',
                  'username', 'email', 'first_name')


class SignupSerializer(serializers.Serializer, UserDataValidation):
    '''Сериализация для auth/sighup.'''
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)
