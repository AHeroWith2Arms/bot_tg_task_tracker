from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


User = get_user_model()


@pytest.mark.django_db
def test_user_registration_and_jwt_login() -> None:
    client = APIClient()
    register_url = reverse("register")
    data = {
        "email": "test@example.com",
        "password": "StrongPass123!",
    }
    response = client.post(register_url, data, format="json")
    assert response.status_code == 201
    assert User.objects.filter(email="test@example.com").exists()

    token_url = reverse("jwt-create")
    token_response = client.post(
        token_url,
        {"email": "test@example.com", "password": "StrongPass123!"},
        format="json",
    )
    assert token_response.status_code == 200
    assert "access" in token_response.data


@pytest.mark.django_db
def test_me_endpoint_returns_current_user() -> None:
    user = User.objects.create_user(
        email="meuser@example.com",
        password="Password123!",
    )
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("me")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["email"] == "meuser@example.com"

