from rest_framework import serializers

from api.validators import ValidationUser


class SignupSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация auth/sighup.'''
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class GettingTokenSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация получения токена.'''
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)
