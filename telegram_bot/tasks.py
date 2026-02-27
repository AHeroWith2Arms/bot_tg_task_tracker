from __future__ import annotations

import datetime as dt
from typing import Iterable

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from habits.models import Habit
from users.models import User


def _format_habit_message(habit: Habit) -> str:
    return f"Напоминание: я буду {habit.action} в {habit.time} в {habit.place}"


def _get_recipients(habits: Iterable[Habit]) -> dict[int, list[Habit]]:
    by_user: dict[int, list[Habit]] = {}
    for habit in habits:
        user_id = habit.user_id
        by_user.setdefault(user_id, []).append(habit)
    return by_user


@shared_task
def send_due_habits_reminders() -> None:
    """
    Периодическая задача Celery.

    Находит привычки, у которых наступило время выполнения сегодня,
    и отправляет напоминания пользователям в Telegram.
    """

    if not settings.TELEGRAM_BOT_TOKEN:
        return

    now = timezone.localtime()
    today_time = dt.time(hour=now.hour, minute=now.minute)

    habits = Habit.objects.filter(time=today_time)
    habits_by_user = _get_recipients(habits)

    if not habits_by_user:
        return

    bot_token = settings.TELEGRAM_BOT_TOKEN
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    users = User.objects.filter(id__in=habits_by_user.keys())
    chat_ids = {u.id: u.telegram_chat_id for u in users if u.telegram_chat_id}

    for user_id, user_habits in habits_by_user.items():
        chat_id = chat_ids.get(user_id)
        if not chat_id:
            continue

        text = "\n".join(_format_habit_message(h) for h in user_habits)
        payload = {"chat_id": chat_id, "text": text}
        try:
            requests.post(base_url, json=payload, timeout=5)
        except requests.RequestException:
            # В проде сюда можно добавить логирование.
            continue

