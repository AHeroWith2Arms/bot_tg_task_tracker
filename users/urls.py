from __future__ import annotations

from django.urls import path

from .views import MeView, RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
]

