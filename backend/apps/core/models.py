"""Shared abstract models for GroupKaro."""
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base with self-managing ``created_at`` / ``updated_at``.

    Every concrete model in the project should inherit from this so the
    timestamps are consistent and DRY. Do NOT add fields here that only
    some models need — this is for universal metadata only.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
