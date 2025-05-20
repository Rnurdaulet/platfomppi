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
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+7 (7XX) XXX-XX-XX"}),
            "email": forms.EmailInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # передаём user из views
        super().__init__(*args, **kwargs)

        if self.user and not self.instance.pk:  # Только при создании
            self.fields["full_name"].initial = f"{self.user.last_name} {self.user.first_name}"


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
