from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("participant", "Участник"),
        ("expert", "Эксперт"),
        ("super_expert", "СуперЭксперт"),
        ("admin", "Админ"),
    ]
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="participant")
