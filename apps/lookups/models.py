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
        return f"{self.name}"


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


class EvaluationCriterion(TranslatableNameMixin, models.Model):
    """
    Справочник критериев оценки заявок.
    Используется в конкурсах для экспертного оценивания.
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Код",
        help_text="Уникальный системный код, латиницей (например: relevance, clarity)"
    )
    name_ru = models.CharField(max_length=255, verbose_name="Название (рус)")
    name_kk = models.CharField(max_length=255, verbose_name="Атауы (қаз)")

    description_ru = models.TextField(verbose_name="Описание (рус)")
    description_kk = models.TextField(verbose_name="Сипаттама (қаз)")

    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        db_table = "lookups_evaluation_criterion"
        verbose_name = "Критерий оценки"
        verbose_name_plural = "Критерии оценки"
        ordering = ["order"]
        indexes = [
            models.Index(fields=["code"], name="idx_evaluationcriterion_code")
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class ExpertRegistry(models.Model):
    """
    Справочник утверждённых экспертов из внешней базы.
    Используется для авторизации и назначения ролей при входе.
    """

    ROLE_CHOICES = [
        ("expert", "Эксперт"),
        ("super_expert", "Суперэксперт"),
    ]

    iin = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="ИИН"
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия"
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Филиал"
    )

    role = models.CharField(
        max_length=32,
        choices=ROLE_CHOICES,
        default="expert",
        verbose_name="Роль"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lookups_expert_registry"
        verbose_name = "Эксперт (реестр)"
        verbose_name_plural = "Эксперты (реестр)"
        ordering = ["branch", "last_name", "first_name"]
        indexes = [
            models.Index(fields=["iin"], name="idx_expert_iin")
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.role})"
