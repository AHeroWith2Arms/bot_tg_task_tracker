from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient

from habits.models import Habit


User = get_user_model()


@pytest.mark.django_db
def test_habit_model_validators() -> None:
    user = User.objects.create_user(
        email="u1@example.com",
        password="Password123!",
    )
    pleasant = Habit.objects.create(
        user=user,
        place="дом",
        time=dt.time(9, 0),
        action="читать",
        is_pleasant=True,
        time_to_complete=60,
        periodicity=1,
    )

    habit = Habit(
        user=user,
        place="улица",
        time=dt.time(10, 0),
        action="гулять",
        linked_habit=pleasant,
        time_to_complete=100,
        periodicity=2,
    )
    habit.clean()

    habit.time_to_complete = 130
    with pytest.raises(ValidationError):
        habit.clean()


@pytest.mark.django_db
def test_habit_crud_and_permissions() -> None:
    user = User.objects.create_user(
        email="owner@example.com",
        password="Password123!",
    )
    other = User.objects.create_user(
        email="other@example.com",
        password="Password123!",
    )
    client = APIClient()
    client.force_authenticate(user=user)

    list_url = reverse("my-habits-list")
    create_data = {
        "place": "дом",
        "time": "09:00:00",
        "action": "читать книгу",
        "is_pleasant": False,
        "periodicity": 1,
        "time_to_complete": 60,
        "is_public": True,
    }
    create_response = client.post(list_url, create_data, format="json")
    assert create_response.status_code == 201
    habit_id = create_response.data["id"]

    response = client.get(list_url)
    assert response.status_code == 200
    assert response.data["count"] == 1

    client.force_authenticate(user=other)
    detail_url = reverse("my-habits-detail", args=[habit_id])
    forbidden_response = client.get(detail_url)
    assert forbidden_response.status_code == 404


@pytest.mark.django_db
def test_public_habits_list_requires_authentication() -> None:
    user = User.objects.create_user(
        email="owner2@example.com",
        password="Password123!",
    )
    Habit.objects.create(
        user=user,
        place="дом",
        time=dt.time(9, 0),
        action="зарядка",
        is_public=True,
        periodicity=1,
        time_to_complete=60,
    )

    client = APIClient()
    url = reverse("public-habits-list")

    # анонимному пользователю доступ запрещён
    anon_response = client.get(url)
    assert anon_response.status_code == 401

    # авторизованному пользователю список доступен
    client.force_authenticate(user=user)
    auth_response = client.get(url)
    assert auth_response.status_code == 200
    assert auth_response.data["count"] == 1

