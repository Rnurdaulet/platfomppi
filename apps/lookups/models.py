from django.db import models
from .mixins import TranslatableNameMixin


class Branch(TranslatableNameMixin, models.Model):
    """
    Справочник филиалов.
    """

    name_ru = models.CharField(max_length=255, verbose_name="Название (рус)")
    name_kk = models.CharField(max_length=255, verbose_name="Атауы (қаз)")
    bin = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="БИН организации",
        help_text="12-значный бизнес-идентификационный номер"
    )
    external_id = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Внешний ID",
        help_text="ID из внешней системы (например, ЕБДП)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        db_table = "lookups_branch"
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
        ordering = ["name_ru"]
        indexes = [
            models.Index(fields=["bin"], name="idx_branch_bin"),
            models.Index(fields=["external_id"], name="idx_branch_external_id")
        ]

    def __str__(self):
        return f"{self.name} ({self.bin})"


class CompetitionDirection(TranslatableNameMixin, models.Model):
    """
    Справочник направлений конкурса.
    """

    name_ru = models.CharField(max_length=255, unique=True, verbose_name="Название (рус)")
    name_kk = models.CharField(max_length=255, unique=True, verbose_name="Атауы (қаз)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        db_table = "lookups_competition_direction"
        verbose_name = "Направление конкурса"
        verbose_name_plural = "Направления конкурса"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name


class QualificationCategory(TranslatableNameMixin, models.Model):
    """
    Справочник квалификационных категорий педагогов.
    """

    name_ru = models.CharField(max_length=255, unique=True, verbose_name="Название (рус)")
    name_kk = models.CharField(max_length=255, unique=True, verbose_name="Атауы (қаз)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        db_table = "lookups_qualification_category"
        verbose_name = "Квалификационная категория"
        verbose_name_plural = "Квалификационные категории"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name
