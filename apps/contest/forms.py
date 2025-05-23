from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.contest.models import Application
from apps.lookups.models import Region, QualificationCategory
from apps.accounts.models import ParticipantProfile


class ApplicationForm(forms.ModelForm):
    # поля из профиля участника
    full_name = forms.CharField(max_length=255, label="Ф.И.О.")
    position = forms.CharField(max_length=255, label="Должность")
    qualification = forms.ModelChoiceField(queryset=QualificationCategory.objects.all(), label="Квалификационная категория")
    organization_name = forms.CharField(max_length=255, label="Название организации")
    organization_address = forms.CharField(max_length=255, label="Адрес организации")
    phone = forms.CharField(max_length=32, label="Телефон")
    email = forms.EmailField(label="Электронная почта")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label="Регион")
    consent = forms.BooleanField(label="Согласие на обработку персональных данных", required=True)

    class Meta:
        model = Application
        exclude = ["uid", "participant", "cms", "is_locked", "submitted_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Предзаполнение из профиля
        if self.user:
            profile = getattr(self.user, "participant_profile", None)
            if profile:
                self.initial.update({
                    "full_name": profile.full_name,
                    "position": profile.position,
                    "qualification": profile.qualification,
                    "organization_name": profile.organization_name,
                    "organization_address": profile.organization_address,
                    "phone": profile.phone,
                    "email": profile.email,
                    "region": profile.region,
                    "consent": profile.consent,
                })
            elif not self.instance.pk:
                self.initial["full_name"] = f"{self.user.last_name} {self.user.first_name}"

        # Добавление CSS-классов и отображение ошибок
        for name, field in self.fields.items():
            base_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                base_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                base_class = "form-select"

            if self.errors.get(name):
                base_class += " is-invalid"
            elif self.is_bound:
                base_class += " is-valid"

            field.widget.attrs.setdefault("class", base_class)

        self.fields["consent"].error_messages = {
            "required": "Необходимо дать согласие на обработку персональных данных."
        }

        # Блокировка при is_locked
        if self.instance and self.instance.is_locked:
            for field in self.fields.values():
                field.disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.is_locked:
            raise ValidationError("Заявка уже подписана и не может быть изменена.")
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            application = super().save(commit=False)
            application.participant = self.user

            # Профиль участника
            profile, _ = ParticipantProfile.objects.get_or_create(user=self.user)
            profile.full_name = self.cleaned_data["full_name"]
            profile.position = self.cleaned_data["position"]
            profile.qualification = self.cleaned_data["qualification"]
            profile.organization_name = self.cleaned_data["organization_name"]
            profile.organization_address = self.cleaned_data["organization_address"]
            profile.phone = self.cleaned_data["phone"]
            profile.email = self.cleaned_data["email"]
            profile.region = self.cleaned_data["region"]
            profile.consent = self.cleaned_data["consent"]
            profile.save()

            # Обновим email в user, если нужно
            if self.user.email != self.cleaned_data["email"]:
                self.user.email = self.cleaned_data["email"]
                self.user.save(update_fields=["email"])

            if commit:
                application.save()

            return application
