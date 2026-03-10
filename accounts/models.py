import random
from datetime import timedelta
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone


# role Based Parmession kichinka yoki Role static bolsa
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
        return self.email

    class Meta:
        db_table = "users"


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name="uuid")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255, null=True, blank=True)
    card_expiration_date = models.DateField(null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.card_number

    class Meta:
        db_table = "cards"


def generate_code():
    # 100000 dan 999999 gacha random son
    return random.randint(100000, 999999)


def exp_time_now():
    # Hozirdan 2 daqiqa keyin muddati tugaydi
    return timezone.now() + timedelta(minutes=2)


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='verification_codes')
    code = models.PositiveIntegerField(default=generate_code)
    expired_date = models.DateTimeField(default=exp_time_now)

    def is_valid(self):
        """Kodning muddati o'tmagan bo'lsa True qaytaradi."""
        return timezone.now() <= self.expired_date

    def __str__(self):
        return f"{self.user.username} — Kod: {self.code}"
