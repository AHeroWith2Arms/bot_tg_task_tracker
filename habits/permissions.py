from __future__ import annotations

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Доступ к объекту только для его владельца."""

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore[override]
        return getattr(obj, "user", None) == request.user

