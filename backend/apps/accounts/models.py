"""Accounts domain: societies, users, and OTP challenges.

Auth design (locked in F0-3)
----------------------------
* Users register with phone + OTP (phone verified once).
* After OTP verification, users choose a ``username`` and ``password``.
* Routine login uses ``username`` + ``password`` (no SMS).
* Password reset reuses phone-OTP.
* The custom ``User`` replaces Django's ``auth.User`` and is wired via
  ``AUTH_USER_MODEL = "accounts.User"`` in settings.

Circular FK note
----------------
There is a circular FK between ``Society`` and ``User``:
    Society.admin_user_id -> User
    User.society_id       -> Society
Both sides are NULLABLE, and the documented insert order is:
    1. create Society (admin_user_id=None)
    2. create admin User (society_id=society.id)
    3. update Society.admin_user_id = user.id
"""

from __future__ import annotations

import secrets
from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.core.constants import UserRole
from apps.core.models import TimeStampedModel

from .managers import UserManager


# ---------------------------------------------------------------------------
# Society
# ---------------------------------------------------------------------------
class Society(TimeStampedModel):
    """A residential society / apartment complex."""

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    admin_user_id = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="administered_societies",
        db_column="admin_user_id",
    )

    invite_code = models.CharField(max_length=20, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "societies"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self._generate_invite_code()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_invite_code() -> str:
        # Excludes ambiguous chars (0/O, 1/I/L) for easy typing
        alphabet = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
        return "".join(secrets.choice(alphabet) for _ in range(8))


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model.

    Login identifier: ``username``.
    Phone: unique, verified once at signup via OTP, reused for password reset.
    """

    # Login credentials
    username = models.CharField(max_length=150, unique=True, db_index=True)
    password = models.CharField(max_length=255)  # noqa: DJ001 — override to be explicit

    # Identity
    phone = models.CharField(max_length=20, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    # Role / society
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.RESIDENT,
    )
    society_id = models.ForeignKey(
        "accounts.Society",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
        db_column="society_id",
    )
    flat_no = models.CharField(max_length=20, blank=True)

    # Django auth flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Whether this user can access the Django admin site.",
    )

    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone", "full_name"]

    class Meta(TimeStampedModel.Meta):
        indexes = [
            models.Index(fields=["society_id", "role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.username} <{self.phone}>"

    @property
    def is_admin_like(self) -> bool:
        """Convenience flag for permission checks (used from F0-5 on)."""
        return self.role in {UserRole.MAIN_ADMIN, UserRole.SOCIETY_ADMIN}


# ---------------------------------------------------------------------------
# OTP
# ---------------------------------------------------------------------------
class OtpCode(TimeStampedModel):
    """A short-lived phone-OTP challenge.

    Used at signup (phone verification) and password reset.
    The raw code is NEVER stored — only a hash.
    """

    phone = models.CharField(max_length=20, db_index=True)
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        indexes = [
            models.Index(fields=["phone", "expires_at"]),
            models.Index(fields=["consumed_at"]),
        ]

    def __str__(self) -> str:
        return f"OTP for {self.phone} (expires {self.expires_at:%Y-%m-%d %H:%M})"

    @property
    def is_expired(self) -> bool:
        from django.utils import timezone
        return self.expires_at <= timezone.now()

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None
