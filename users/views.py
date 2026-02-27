from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class MeView(generics.RetrieveUpdateAPIView):
    """Просмотр и изменение профиля текущего пользователя."""

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

