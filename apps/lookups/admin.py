from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Branch, CompetitionDirection, QualificationCategory, EvaluationCriterion, ExpertRegistry, Region, \
    Subject, SchoolType, SchoolForm, Location, Position, School


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ("name_ru", "code")
    search_fields = ("name_ru", "name_kk", "code")


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "bin", "external_id", "region", "created_at")  # <- добавлено
    search_fields = ("name_ru", "name_kk", "bin", "external_id", "region__name_ru")  # <- по имени региона
    list_filter = ("region", "created_at")  # <- фильтр по региону
    ordering = ("name_ru",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name_ru", "name_kk", "bin", "external_id", "region")  # <- добавлено
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


@admin.register(EvaluationCriterion)
class EvaluationCriterionAdmin(ModelAdmin):
    list_display = ("code", "name_ru", "name_kk", "order", "created_at")
    search_fields = ("code", "name_ru", "name_kk")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("code", "name_ru", "name_kk", "description_ru", "description_kk", "order")
        }),
        ("Служебное", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(ExpertRegistry)
class ExpertRegistryAdmin(ModelAdmin):
    list_display = ("iin", "last_name", "first_name", "role", "branch")
    search_fields = ("iin", "last_name", "first_name")
    list_filter = ("role", "branch")
    ordering = ("branch", "last_name", "first_name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("iin", "last_name", "first_name", "role", "branch")
        }),
        ("Служебная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "external_id")
    search_fields = ("name_ru", "name_kk")
    ordering = ("name_ru",)


@admin.register(SchoolType)
class SchoolTypeAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "external_id")
    search_fields = ("name_ru", "name_kk")
    ordering = ("external_id",)


@admin.register(SchoolForm)
class SchoolFormAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "external_id")
    search_fields = ("name_ru", "name_kk")
    ordering = ("external_id",)


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "external_id")
    search_fields = ("name_ru", "name_kk")
    ordering = ("external_id",)


@admin.register(Position)
class PositionAdmin(ModelAdmin):
    list_display = ("name_ru", "name_kk", "external_id")
    search_fields = ("name_ru", "name_kk")
    ordering = ("name_ru",)


@admin.register(School)
class SchoolAdmin(ModelAdmin):
    list_display = ("name_ru", "region", "location", "school_type", "school_form", "external_id")
    search_fields = ("name_ru", "name_kk", "external_id")
    list_filter = ("region", "school_type", "school_form")
    ordering = ("name_ru",)

    fieldsets = (
        (None, {
            "fields": ("name_ru", "name_kk", "region", "location", "school_type", "school_form", "external_id")
        }),
    )
