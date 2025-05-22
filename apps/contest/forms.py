from django import forms
from apps.contest.models import Application
from django.core.exceptions import ValidationError


class ApplicationForm(forms.ModelForm):
    """
    Форма подачи заявки участником. Без CMS и без is_locked.
    """

    class Meta:
        model = Application
        exclude = ["uid", "participant", "cms", "is_locked", "submitted_at", "updated_at"]
        widgets = {
            "consent": forms.CheckboxInput(attrs={"class": "checkbox"}),
            "phone": forms.TextInput(attrs={   "class": "form-control form-control-lg",
    "type": "tel",
    "placeholder": "+7 (7XX) XXX-XX-XX",
    "id": "phone"}),
            "email": forms.EmailInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # передаём user из views
        super().__init__(*args, **kwargs)

        # Ф.И.О. участника
        self.fields["full_name"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "Иванов Иван"
        })

        # Электронная почта
        self.fields["email"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "email@example.com"
        })

        # Телефон
        self.fields["phone"].widget.attrs.update({
            "class": "form-control ",
            "type": "tel",
            "placeholder": "+7 (7XX) XXX-XX-XX"
        })

        # Должность
        self.fields["position"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "Учитель информатики"
        })

        # Квалификационная категория
        self.fields["qualification"].widget.attrs.update({
            "class": "form-select "
        })

        # Филиал
        self.fields["branch"].widget.attrs.update({
            "class": "form-select "
        })

        # Название организации
        self.fields["organization_name"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "КГУ 'Школа №5'"
        })

        # Адрес организации
        self.fields["organization_address"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "г. Алматы, ул. Абая, 25"
        })

        # Название конкурсного материала
        self.fields["title"].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "Разработка урока по математике"
        })

        # Направление конкурса
        self.fields["direction"].widget.attrs.update({
            "class": "form-select "
        })

        # Файл заявки
        self.fields["file"].widget.attrs.update({
            "class": "form-control "
        })

        # Согласие
        self.fields["consent"].widget.attrs.update({
            "class": "form-check-input"
        })
        self.fields["consent"].required = True
        self.fields["consent"].error_messages = {
            "required": "Необходимо дать согласие на обработку персональных данных."
        }

        for name, field in self.fields.items():
            css_class = "form-control "
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                css_class = "form-select "

            if self.errors.get(name):
                css_class += " is-invalid"
            elif self.is_bound:
                css_class += " is-valid"

            field.widget.attrs["class"] = css_class.strip()

        # Автозаполнение ФИО
        if self.user and not self.instance.pk:
            self.fields["full_name"].initial = f"{self.user.last_name} {self.user.first_name}"

        # Блокировка формы при is_locked
        if self.instance and self.instance.is_locked:
            for field in self.fields.values():
                field.disabled = True

    def clean_participant(self):
        # Просто на случай, если кто-то вручную подставит participant
        participant = self.cleaned_data.get("participant")
        if participant and participant.role != "participant":
            raise ValidationError("Только участник может подать заявку.")
        return participant

    def clean(self):
        cleaned_data = super().clean()

        if self.instance and self.instance.is_locked:
            raise ValidationError("Заявка уже подписана и не может быть изменена.")

        return cleaned_data
