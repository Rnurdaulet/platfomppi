import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.lookups.models import Branch, QualificationCategory, Region, Position, Subject, School


class User(AbstractUser):
    """
    Кастомная модель пользователя с ролями, отчеством и опциональной привязкой к филиалу.
    """

    ROLE_CHOICES = [
        ("participant", _("Участник")),
        ("expert", _("Эксперт")),
        ("super_expert", _("СуперЭксперт")),
        ("admin", _("Админ")),
    ]

    role = models.CharField(
        max_length=32,
        choices=ROLE_CHOICES,
        default="participant",
        verbose_name=_("Роль")
    )

    middlename = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Отчество")
    )

    class Meta:
        db_table = "accounts_user"
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ["-date_joined"]

    @staticmethod
    def generate_nonce(length=16):
        """Генерация безопасного nonce"""
        return secrets.token_urlsafe(length)

    @property
    def profile(self):
        if self.role == "participant":
            return getattr(self, "participant_profile", None)
        return None

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middlename:
            full_name += f" {self.middlename}"
        return f"{full_name.strip()} ({self.get_role_display()})"


class ParticipantProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="participant_profile",
        limit_choices_to={"role": "participant"},
        verbose_name="Пользователь"
    )

    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О. (из ЭЦП)")
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Должность"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Предмет"
    )
    qualification = models.ForeignKey(
        QualificationCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Квалификационная категория"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Школа / Учреждение"
    )
    organization_name = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name="Название организации вручную"
    )
    not_found_school = models.BooleanField(default=True, verbose_name="Не нашёл организацию в справочнике")

    organization_address = models.CharField(max_length=255, verbose_name="Адрес организации образования")
    phone = models.CharField(max_length=32, verbose_name="Контактный телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Регион"
    )
    consent = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")

    class Meta:
        db_table = "participant_profile"
        verbose_name = "Профиль участника"
        verbose_name_plural = "Профили участников"

    def __str__(self):
        return f"{self.full_name} — {self.user.username}"
