from django.db import models
from .mixins import TranslatableNameMixin
from django.utils.translation import gettext_lazy as _

class Region(TranslatableNameMixin, models.Model):
    """
    Справочник регионов.
    """

    name_ru = models.CharField(max_length=255, verbose_name="Название региона (рус)")
    name_kk = models.CharField(max_length=255, verbose_name="Атауы (қаз)")
    code = models.CharField(max_length=10, unique=True, verbose_name="Код региона")
    external_id = models.CharField(
        max_length=64,
        verbose_name="Внешний ID",
        help_text="ID из внешней системы (например, ЕБДП)",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "lookups_region"
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ["name_ru"]

    def __str__(self):
        return f"{self.name}"


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
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="branches",
        verbose_name="Регион",
        null=True,
        blank=True
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

class AdminRegistry(models.Model):
    """
    Справочник утверждённых администраторов.
    Используется для авторизации и назначения роли 'admin' при входе.
    """

    iin = models.CharField(
        max_length=12,
        unique=True,
        verbose_name=_("ИИН")
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Фамилия")
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_("Имя")
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Филиал")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lookups_admin_registry"
        verbose_name = _("Администратор (реестр)")
        verbose_name_plural = _("Администраторы (реестр)")
        ordering = ["branch", "last_name", "first_name"]
        indexes = [
            models.Index(fields=["iin"], name="idx_admin_iin")
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} (admin)"

    @property
    def role(self):
        return "admin"

class Subject(TranslatableNameMixin, models.Model):
    name_ru = models.CharField(max_length=255, verbose_name="Название (рус.)")
    name_kk = models.CharField(max_length=255, verbose_name="Атауы (қаз.)")
    external_id = models.PositiveIntegerField(unique=True, verbose_name="Внешний ID")

    class Meta:
        db_table = "lookup_subject"
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name


class SchoolType(TranslatableNameMixin, models.Model):
    name_ru = models.CharField(max_length=255, verbose_name="Тип организации (рус.)")
    name_kk = models.CharField(max_length=255, verbose_name="Ұйым түрі (қаз.)")
    external_id = models.PositiveIntegerField(unique=True, verbose_name="Внешний ID")

    class Meta:
        db_table = "lookup_school_type"
        verbose_name = "Тип учебной организации"
        verbose_name_plural = "Типы учебных организаций"
        ordering = ["external_id"]

    def __str__(self):
        return self.name


class SchoolForm(TranslatableNameMixin, models.Model):
    name_ru = models.CharField(max_length=255, verbose_name="Форма (рус.)")
    name_kk = models.CharField(max_length=255, verbose_name="Форма (қаз.)")
    external_id = models.PositiveIntegerField(unique=True, verbose_name="Внешний ID")

    class Meta:
        db_table = "lookup_school_form"
        verbose_name = "Форма организации"
        verbose_name_plural = "Формы организаций"
        ordering = ["external_id"]

    def __str__(self):
        return self.name


class Location(TranslatableNameMixin, models.Model):
    name_ru = models.CharField(max_length=255, verbose_name="Форма (рус.)")
    name_kk = models.CharField(max_length=255, verbose_name="Форма (қаз.)")
    external_id = models.PositiveIntegerField(unique=True, verbose_name="Внешний ID")

    class Meta:
        db_table = "lookup_location"
        verbose_name = "Населённый пункт / Район"
        verbose_name_plural = "Населённые пункты / Районы"
        ordering = ["external_id"]

    def __str__(self):
        return self.name_ru


class Position(TranslatableNameMixin, models.Model):
    name_ru = models.CharField(max_length=255, verbose_name="Должность (рус.)")
    name_kk = models.CharField(max_length=255, verbose_name="Лауазымы (қаз.)")
    external_id = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "lookup_position"
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name


class School(TranslatableNameMixin,models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name="Регион")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 verbose_name="Населённый пункт / Район")
    name_kk = models.CharField(max_length=512, verbose_name="Атауы (қаз.)")
    name_ru = models.CharField(max_length=512, verbose_name="Название (рус.)")

    school_type = models.ForeignKey(SchoolType, on_delete=models.SET_NULL, null=True, verbose_name="Тип организации")
    school_form = models.ForeignKey(SchoolForm, on_delete=models.SET_NULL, null=True, verbose_name="Форма организации")

    external_id = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "lookup_school"
        verbose_name = "Школа / Учреждение"
        verbose_name_plural = "Школы / Учреждения"
        ordering = ["name_ru"]

    def __str__(self):
        return self.name_ru
