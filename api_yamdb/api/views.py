from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .serializers import GettingTokenSerializer, SignupSerializer


class SignupUserAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя """
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
        except IntegrityError:
            msg = 'Пользователь с такими данными уже существует'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        send_mail(
            subject='Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAuthApiView(generics.CreateAPIView):
    """Получение токена """
    serializer_class = GettingTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
