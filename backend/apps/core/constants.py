"""Shared enumerations for GroupKaro."""

from django.db import models


class UserRole(models.TextChoices):
    MAIN_ADMIN = "main_admin", "Main Admin"
    SOCIETY_ADMIN = "society_admin", "Society Admin"
    RESIDENT = "resident", "Resident"
    VENDOR = "vendor", "Vendor"


class PoolStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    OPEN = "open", "Open"
    THRESHOLD_MET = "threshold_met", "Threshold Met"
    SOURCING = "sourcing", "Sourcing"
    CONFIRMED = "confirmed", "Confirmed"
    COLLECTING_PAYMENT = "collecting_payment", "Collecting Payment"
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    EXPIRED = "expired", "Expired"


class PoolType(models.TextChoices):
    SOCIETY_WIDE = "society_wide", "Society Wide"
    CUSTOM = "custom", "Custom"


class PaymentStatus(models.TextChoices):
    PLEDGED = "pledged", "Pledged"
    PAID = "paid", "Paid"
    REFUNDED = "refunded", "Refunded"


class PaymentMethod(models.TextChoices):
    MANUAL_TRANSFER = "manual_transfer", "Manual Transfer"
    JAZZCASH = "jazzcash", "JazzCash"
    EASYPAISA = "easypaisa", "EasyPaisa"
    BANK = "bank", "Bank Transfer"


class PaymentRecordStatus(models.TextChoices):
    RECORDED = "recorded", "Recorded"
    REFUNDED = "refunded", "Refunded"


class BidStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    WITHDRAWN = "withdrawn", "Withdrawn"


class PayoutStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"


class NotificationType(models.TextChoices):
    POOL_THRESHOLD_MET = "pool_threshold_met", "Pool Threshold Met"
    POOL_CONFIRMED = "pool_confirmed", "Pool Confirmed"
    POOL_SCHEDULED = "pool_scheduled", "Pool Scheduled"
    POOL_COMPLETED = "pool_completed", "Pool Completed"
    POOL_CANCELLED = "pool_cancelled", "Pool Cancelled"
    POOL_EXPIRED = "pool_expired", "Pool Expired"
    PAYMENT_RECORDED = "payment_recorded", "Payment Recorded"
