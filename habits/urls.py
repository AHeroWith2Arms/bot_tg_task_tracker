from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register("my", HabitViewSet, basename="my-habits")
router.register("public", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path("", include(router.urls)),
]

