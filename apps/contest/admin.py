from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.contest.models import Application


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = (
        "uid",
        "get_full_name",
        "title",
        "get_region",
        "direction",
        "get_qualification",
        "is_locked",
        "submitted_at",
    )
    list_filter = (
        "direction",
        "is_locked",
        "participant__participant_profile__region",
        "participant__participant_profile__qualification",
    )
    search_fields = (
        "uid",
        "title",
        "participant__participant_profile__full_name",
        "participant__participant_profile__email",
        "participant__participant_profile__phone",
    )
    ordering = ("-submitted_at",)

    def get_readonly_fields(self, request, obj=None):
        base_fields = (
            "uid",
            "submitted_at",
            "updated_at",
            "participant",
            "cms",
        )
        profile_fields = (
            "get_full_name",
            "get_position",
            "get_email",
            "get_phone",
            "get_org_name",
            "get_org_address",
            "get_consent",
            "get_region",
            "get_qualification",
        )
        return base_fields + profile_fields if obj else base_fields

    fieldsets = (
        ("Идентификатор", {
            "fields": ("uid", "participant", "is_locked")
        }),
        ("Регион и категория", {
            "fields": ("direction",)
        }),
        ("Материал", {
            "fields": ("title", "file", "cms")
        }),
        ("Техническая информация", {
            "fields": ("submitted_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    # Методы для отображения связанных полей
    def get_profile(self, obj):
        return getattr(obj.participant, "participant_profile", None)

    def get_full_name(self, obj):
        profile = self.get_profile(obj)
        return profile.full_name if profile else "—"
    get_full_name.short_description = "Ф.И.О."

    def get_position(self, obj):
        profile = self.get_profile(obj)
        return profile.position if profile else "—"
    get_position.short_description = "Должность"

    def get_email(self, obj):
        profile = self.get_profile(obj)
        return profile.email if profile else "—"
    get_email.short_description = "Email"

    def get_phone(self, obj):
        profile = self.get_profile(obj)
        return profile.phone if profile else "—"
    get_phone.short_description = "Телефон"

    def get_org_name(self, obj):
        profile = self.get_profile(obj)
        return profile.organization_name if profile else "—"
    get_org_name.short_description = "Организация"

    def get_org_address(self, obj):
        profile = self.get_profile(obj)
        return profile.organization_address if profile else "—"
    get_org_address.short_description = "Адрес организации"

    def get_consent(self, obj):
        profile = self.get_profile(obj)
        return "✅" if profile and profile.consent else "❌"
    get_consent.short_description = "Согласие"

    def get_region(self, obj):
        profile = self.get_profile(obj)
        return profile.region if profile else "—"
    get_region.short_description = "Регион"

    def get_qualification(self, obj):
        profile = self.get_profile(obj)
        return profile.qualification if profile else "—"
    get_qualification.short_description = "Категория"
