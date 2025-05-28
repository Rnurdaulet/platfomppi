from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.lookups.models import Branch, CompetitionDirection, QualificationCategory
from apps.contest.validators import validate_word_file
from apps.contest.utils import generate_short_uid
from django.conf import settings
from datetime import date


def application_upload_path(instance, filename):
    return f"applications/{instance.uid}/{filename}"


class Application(models.Model):
    uid = models.CharField(
        max_length=22,
        unique=True,
        default=generate_short_uid,
        editable=False,
        verbose_name=_("UID")
    )

    participant = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        limit_choices_to={"role": "participant"},
        verbose_name=_("Участник")
    )

    direction = models.ForeignKey(
        CompetitionDirection,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Направление конкурса")
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_("Название конкурсного материала")
    )
    keywords = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_("Ключевые слова"),
        help_text=_("Укажите ключевые слова через запятую")
    )
    file = models.FileField(
        upload_to=application_upload_path,
        validators=[validate_word_file],
        verbose_name=_("Файл заявки (.docx/.doc)"),
        help_text=_("Формат .docx/.doc, до 5 МБ")
    )

    cms = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Подпись (CMS)")
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_("Заявка отправлена (заблокирована)")
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата подачи")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Обновлено")
    )

    class Meta:
        db_table = "contest_application"
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.uid} — {self.participant.profile.full_name} — {self.title}"

    def can_edit(self) -> bool:
        """Можно ли редактировать заявку"""
        if self.is_locked:
            return False
        return date.today() < getattr(settings, "APPLICATION_EDIT_DEADLINE", date.max)
