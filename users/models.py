from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель пользователя с авторизацией по email и chat_id Telegram."""

    # Используем email как уникальный идентификатор вместо username
    username = None
    email = models.EmailField(_("email address"), unique=True)

    telegram_chat_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Идентификатор чата пользователя в Telegram.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        return self.email

