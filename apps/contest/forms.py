import logging
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import ParticipantProfile
from apps.contest.models import Application
from apps.lookups.models import Region, QualificationCategory, School, Position, Subject
from utils.tasks import send_application_accepted_task, send_application_updated_task

logger = logging.getLogger(__name__)


class ApplicationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, label=_("Ф.И.О."))

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label=_("Должность"),
        widget=autocomplete.ModelSelect2(
            url="position-autocomplete",
            attrs={"data-theme": "bootstrap-5", "data-width": "100%"}
        )
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label=_("Предмет"),
        required=False,
        widget=autocomplete.ModelSelect2(
            url="subject-autocomplete",
            attrs={"data-theme": "bootstrap-5", "data-width": "100%"}
        )
    )

    school = forms.ModelChoiceField(
        queryset=School.objects.none(),
        label=_("Организация образования"),
        widget=autocomplete.ModelSelect2(
            url="school-autocomplete",
            forward=["region"],
            attrs={"data-theme": "bootstrap-5", "data-width": "100%"}
        )
    )

    organization_name = forms.CharField(
        max_length=255,
        label=_("Название организации вручную"),
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Если не нашли в списке")})
    )

    not_found_school = forms.BooleanField(
        required=False,
        label=_("Не нашёл свою организацию")
    )

    organization_address = forms.CharField(max_length=255, label=_("Адрес организации"))
    phone = forms.CharField(max_length=32, label=_("Телефон"))
    email = forms.EmailField(label=_("Электронная почта"))
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        label=_("Регион"),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    qualification = forms.ModelChoiceField(
        queryset=QualificationCategory.objects.all(),
        label=_("Квалификационная категория")
    )

    consent = forms.BooleanField(
        label=mark_safe(_('Я ознакомлен(а) и соглашаюсь с <a href="/privacy" target="_blank">политикой конфиденциальности</a>.')),
        required=True
    )

    class Meta:
        model = Application
        exclude = ["uid", "participant", "cms", "is_locked", "submitted_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "user must be passed to ApplicationForm"
        logger.debug("Initializing ApplicationForm for user=%s", self.user)

        super().__init__(*args, **kwargs)

        profile = getattr(self.user, "participant_profile", None)
        if profile:
            logger.debug("Pre-filling form from profile %s", profile)
            self.initial.update({
                "full_name": profile.full_name,
                "position": profile.position,
                "subject": getattr(profile, "subject", None),
                "school": getattr(profile, "school", None),
                "organization_address": profile.organization_address,
                "phone": profile.phone,
                "email": profile.email,
                "region": profile.region,
                "qualification": profile.qualification,
                "consent": profile.consent,
                "organization_name": profile.organization_name if profile.not_found_school else "",
                "not_found_school": profile.not_found_school,
            })
        elif not self.instance.pk:
            self.initial["full_name"] = f"{self.user.last_name} {self.user.first_name} {self.user.middlename}"

        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["school"].queryset = School.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                logger.warning("Invalid region id: %s", self.data.get("region"))
                self.fields["school"].queryset = School.objects.none()
        elif profile and profile.region:
            self.fields["school"].queryset = School.objects.filter(region=profile.region)

        self.fields["school"].required = not self.data.get("not_found_school")
        self.fields["phone"].widget.attrs.update({"id": "phone",    "placeholder": "+7 (___) ___-__-__"})
        self.fields["file"].widget.attrs["accept"] = ".doc,.docx"

        # Styling
        for name, field in self.fields.items():
            base_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                base_class = "form-check-input"
            elif isinstance(field.widget, (forms.Select, autocomplete.ModelSelect2)):
                base_class = "form-select"
            if self.errors.get(name):
                base_class += " is-invalid"
            elif self.is_bound:
                base_class += " is-valid"
            field.widget.attrs.setdefault("class", base_class)

    def clean(self):
        cleaned_data = super().clean()
        logger.debug("Running clean() for ApplicationForm")

        not_found_school = cleaned_data.get("not_found_school", False)

        if not_found_school:
            logger.debug("Manual school entry selected (checkbox checked).")
            cleaned_data["school"] = None
        else:
            if not cleaned_data.get("school"):
                logger.warning("School not selected despite checkbox unchecked.")
                self.add_error("school", _("Выберите организацию из списка."))
            cleaned_data["organization_name"] = ""

        if self.instance and self.instance.is_locked:
            logger.error("Attempt to edit locked application (id=%s)", self.instance.pk)
            raise ValidationError(_("Заявка уже подписана и не может быть изменена."))

        return cleaned_data

    def save(self, commit=True):
        logger.debug("Saving ApplicationForm for user=%s", self.user)
        is_new = self.instance.pk is None

        with transaction.atomic():
            application = super().save(commit=False)
            application.participant = self.user
            profile, _ = ParticipantProfile.objects.get_or_create(user=self.user)

            logger.debug("Updating participant profile for user=%s", self.user)

            profile.full_name = self.cleaned_data["full_name"]
            profile.position = self.cleaned_data["position"]
            profile.subject = self.cleaned_data.get("subject")
            profile.organization_address = self.cleaned_data["organization_address"]
            profile.phone = self.cleaned_data["phone"]
            profile.email = self.cleaned_data["email"]
            profile.region = self.cleaned_data["region"]
            profile.qualification = self.cleaned_data["qualification"]
            profile.consent = self.cleaned_data["consent"]
            profile.not_found_school = self.cleaned_data.get("not_found_school", False)

            if profile.not_found_school:
                profile.school = None
                profile.organization_name = self.cleaned_data["organization_name"]
            else:
                profile.school = self.cleaned_data["school"]
                profile.organization_name = ""

            profile.save()

            new_email = self.cleaned_data.get("email")
            if new_email and self.user.email != new_email:
                logger.info("Updating user email: %s → %s", self.user.email, new_email)
                self.user.email = new_email
                self.user.save(update_fields=["email"])

            if commit:
                application.save()
                logger.info("Application saved (id=%s)", application.pk)

        if is_new:
            logger.info("Sending new application email to %s", self.user.email)
            send_application_accepted_task.delay(self.user.email, profile.full_name)
        else:
            logger.info("Sending update email to %s", self.user.email)
            send_application_updated_task.delay(self.user.email, profile.full_name)

        return application
