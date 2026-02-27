from __future__ import annotations

from datetime import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """
    Модель привычки.

    Формула: я буду [action] в [time] в [place].
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField("Место", max_length=255)
    time = models.TimeField("Время", default=time(9, 0))
    action = models.CharField("Действие", max_length=255)

    is_pleasant = models.BooleanField(
        "Приятная привычка",
        default=False,
        help_text="Приятная (вознаграждающая) привычка.",
    )

    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="base_habits",
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, выполняемая в качестве вознаграждения.",
    )

    periodicity = models.PositiveSmallIntegerField(
        "Периодичность (дни)",
        default=1,
        help_text="Как часто напоминать о привычке (в днях, от 1 до 7).",
    )

    reward = models.CharField(
        "Вознаграждение",
        max_length=255,
        blank=True,
        null=True,
    )

    time_to_complete = models.PositiveIntegerField(
        "Время на выполнение (секунды)",
        default=60,
        help_text="Не больше 120 секунд.",
    )

    is_public = models.BooleanField(
        "Публичная привычка",
        default=False,
        help_text="Публичные привычки видны всем пользователям.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("-created_at",)

    def clean(self) -> None:
        errors: dict[str, str] = {}

        if self.reward and self.linked_habit:
            errors["reward"] = "Нельзя одновременно указывать вознаграждение и связанную привычку."
            errors["linked_habit"] = (
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )

        if self.time_to_complete and self.time_to_complete > 120:
            errors["time_to_complete"] = "Время на выполнение не может превышать 120 секунд."

        if self.periodicity and self.periodicity > 7:
            errors["periodicity"] = "Нельзя выполнять привычку реже, чем раз в 7 дней."

        if self.periodicity and self.periodicity < 1:
            errors["periodicity"] = "Периодичность должна быть не реже одного раза в день."

        if self.linked_habit and not self.linked_habit.is_pleasant:
            errors["linked_habit"] = "Связанной может быть только приятная привычка."

        if self.is_pleasant and (self.reward or self.linked_habit):
            errors["is_pleasant"] = (
                "У приятной привычки не может быть отдельного вознаграждения "
                "или другой связанной привычки."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.user}: я буду {self.action} в {self.time} в {self.place}"

