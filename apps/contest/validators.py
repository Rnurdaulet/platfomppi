from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_word_file(file):
    max_size = 5 * 1024 * 1024  # 5MB
    allowed_extensions = [".docx", ".doc"]

    if file.size > max_size:
        raise ValidationError(
            _("Размер файла не должен превышать 5 МБ.")
        )

    if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError(
            _("Файл должен быть в формате .docx или .doc")
        )
