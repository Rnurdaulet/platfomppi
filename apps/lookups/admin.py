from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Branch, CompetitionDirection, QualificationCategory


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "bin", "external_id", "created_at")
    search_fields = ("name_ru", "name_kk", "bin", "external_id")
    list_filter = ("created_at",)
    ordering = ("name_ru",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name_ru", "name_kk", "bin", "external_id")
        }),
        ("Служебная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(CompetitionDirection)
class CompetitionDirectionAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "created_at")
    search_fields = ("name_ru", "name_kk")
    list_filter = ("created_at",)
    ordering = ("name_ru",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name_ru", "name_kk")
        }),
        ("Служебная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(QualificationCategory)
class QualificationCategoryAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "created_at")
    search_fields = ("name_ru", "name_kk")
    list_filter = ("created_at",)
    ordering = ("name_ru",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name_ru", "name_kk")
        }),
        ("Служебная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
