from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class RoleChoice(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    POSTER = 'poster', 'Poster'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid4, verbose_name="uuid"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    passport_number = models.CharField(max_length=255, null=True, blank=True)
    pin = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    telegram_address = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=255, choices=RoleChoice, default=RoleChoice.POSTER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = "users"
