import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя с ролями и опциональной привязкой к филиалу.
    """

    ROLE_CHOICES = [
        ("participant", "Участник"),
        ("expert", "Эксперт"),
        ("super_expert", "СуперЭксперт"),
        ("admin", "Админ"),
    ]

    role = models.CharField(
        max_length=32,
        choices=ROLE_CHOICES,
        default="participant",
        verbose_name="Роль"
    )

    class Meta:
        db_table = "accounts_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    @staticmethod
    def generate_nonce(length=16):
        """Генерация безопасного nonce"""
        return secrets.token_urlsafe(length)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
