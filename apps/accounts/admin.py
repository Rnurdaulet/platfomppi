# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from .models import User
from ..lookups.models import AdminRegistry


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ("username", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Персональные данные", {"fields": ("first_name", "last_name","middlename", "email", "role")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Прочее", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "role", "is_staff", "is_superuser", "groups"),
        }),
    )


from apps.accounts.models import ParticipantProfile


@admin.register(ParticipantProfile)
class ParticipantProfileAdmin(ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "email",
        "phone",
        "region",
        "qualification",
        "position",
        "subject",
        "school",
        "consent",
    )
    list_filter = (
        "region",
        "qualification",
        "consent",
    )
    list_select_related = ("user", "qualification", "region", "position", "subject", "school")

    search_fields = (
        "full_name",
        "user__username",
        "email",
        "phone"
    )
    autocomplete_fields = ("user", "qualification", "region", "position", "subject", "school")

    fieldsets = (
        ("Пользователь", {
            "fields": ("user", "full_name", "email", "phone", "consent")
        }),
        ("Организация", {
            "fields": ("school", "organization_name","organization_address")
        }),
        ("Регион и квалификация", {
            "fields": ("region", "qualification", "position", "subject")
        }),
    )

    readonly_fields = ("user",)
    ordering = ("full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Получаем регион через филиал администратора
        admin_entry = AdminRegistry.objects.select_related("branch__region").filter(iin=request.user.username).first()

        if admin_entry and admin_entry.branch and admin_entry.branch.region:
            return qs.filter(region=admin_entry.branch.region)

        return qs.none()