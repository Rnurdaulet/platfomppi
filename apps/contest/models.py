from django.db import models
from apps.accounts.models import User
from apps.lookups.models import Branch, CompetitionDirection, QualificationCategory
from apps.contest.validators import validate_word_file
from apps.contest.utils import generate_short_uid


def application_upload_path(instance, filename):
    return f"applications/{instance.participant.username}/{filename}"


class Application(models.Model):
    """
    Заявка участника на конкурс. После отправки редактирование невозможно.
    """

    uid = models.CharField(
        max_length=22,
        unique=True,
        default=generate_short_uid,
        editable=False,
        verbose_name="UID"
    )

    participant = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "participant"},
        related_name="application",
        verbose_name="Участник"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Филиал"
    )

    direction = models.ForeignKey(
        CompetitionDirection,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Направление конкурса"
    )

    qualification = models.ForeignKey(
        QualificationCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Квалификационная категория"
    )

    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О. участника (из ЭЦП)")
    position = models.CharField(max_length=255, verbose_name="Должность")
    organization_name = models.CharField(max_length=255, verbose_name="Название организации образования")
    organization_address = models.CharField(max_length=255, verbose_name="Адрес организации образования")
    email = models.EmailField(verbose_name="Электронная почта")
    phone = models.CharField(max_length=32, verbose_name="Контактный телефон")
    consent = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")

    title = models.CharField(max_length=255, verbose_name="Название конкурсного материала")

    file = models.FileField(
        upload_to=application_upload_path,
        validators=[validate_word_file],
        verbose_name="Файл заявки (.docx)",
        help_text="Формат .docx/.doc, до 5 МБ"
    )

    cms = models.TextField(blank=True, null=True, verbose_name="Подпись (CMS)")
    is_locked = models.BooleanField(default=False, verbose_name="Заявка отправлена (заблокирована)")

    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        db_table = "contest_application"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["uid"], name="idx_app_uid"),
            models.Index(fields=["branch"], name="idx_app_branch"),
            models.Index(fields=["direction"], name="idx_app_direction"),
            models.Index(fields=["qualification"], name="idx_app_qualification"),
            models.Index(fields=["submitted_at"], name="idx_app_submitted"),
            models.Index(fields=["is_locked"], name="idx_app_locked"),
        ]

    def __str__(self):
        return f"{self.uid} — {self.full_name} — {self.title}"

    def can_edit(self) -> bool:
        return not self.is_locked
