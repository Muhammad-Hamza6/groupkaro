"""Custom manager for the User model."""
from __future__ import annotations

from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for ``apps.accounts.User``.

    Uses ``username`` as the login identifier (via ``USERNAME_FIELD``) but
    also requires ``phone`` — kept unique and verified at signup.
    """

    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        phone: str,
        password: str | None,
        **extra: Any,
    ) -> "User":  # noqa: F821 — forward ref resolved at runtime
        if not username:
            raise ValueError("username is required")
        if not phone:
            raise ValueError("phone is required")

        normalised_phone = phone.strip().replace(" ", "").replace("-", "")
        user = self.model(
            username=username.strip(),
            phone=normalised_phone,
            **extra,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        phone: str,
        password: str | None = None,
        **extra: Any,
    ) -> "User":
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(username, phone, password, **extra)

    def create_superuser(
        self,
        username: str,
        phone: str,
        password: str | None = None,
        **extra: Any,
    ) -> "User":
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("role", "main_admin")
        if extra.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, phone, password, **extra)
