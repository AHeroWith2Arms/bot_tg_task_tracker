from __future__ import annotations

from rest_framework import mixins, permissions, viewsets

from .models import Habit
from .permissions import IsOwner
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Список публичных привычек (read-only)."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

