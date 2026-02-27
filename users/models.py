from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с chat_id Telegram."""

    telegram_chat_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Идентификатор чата пользователя в Telegram.",
    )

    def __str__(self) -> str:
        return self.username

