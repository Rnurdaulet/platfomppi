from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.contest.models import Application


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = (
        "uid",
        "full_name",
        "title",
        "branch",
        "direction",
        "qualification",
        "is_locked",
        "submitted_at",
    )
    list_filter = (
        "branch",
        "direction",
        "qualification",
        "is_locked",
    )
    search_fields = (
        "uid",
        "full_name",
        "title",
        "email",
        "phone",
    )
    ordering = ("-submitted_at",)
    readonly_fields = (
        "uid",
        "submitted_at",
        "updated_at",
        "participant",
        "cms",
    )

    fieldsets = (
        ("Идентификатор", {
            "fields": ("uid", "participant", "is_locked")
        }),
        ("Филиал и категория", {
            "fields": ("branch", "direction", "qualification")
        }),
        ("Участник", {
            "fields": ("full_name", "position", "email", "phone")
        }),
        ("Организация", {
            "fields": ("organization_name", "organization_address")
        }),
        ("Материал", {
            "fields": ("title", "file", "cms")
        }),
        ("Согласие", {
            "fields": ("consent",)
        }),
        ("Техническая информация", {
            "fields": ("submitted_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
