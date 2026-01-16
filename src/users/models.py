from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Telegram chat id для уведомлений",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
