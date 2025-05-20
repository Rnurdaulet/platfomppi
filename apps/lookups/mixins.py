from django.utils.translation import get_language


class TranslatableNameMixin:
    """
    Добавляет универсальное поле `.name` на основе name_ru / name_kk.
    Упрощает локализованный вывод имени объекта.
    """

    @property
    def name(self) -> str:
        lang = get_language()
        if hasattr(self, "name_kk") and hasattr(self, "name_ru"):
            return self.name_kk if lang == "kk" else self.name_ru
        raise AttributeError("Model must have 'name_ru' and 'name_kk' fields to use TranslatableNameMixin.")
