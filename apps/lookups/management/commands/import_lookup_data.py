import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.lookups.models import Branch, CompetitionDirection, QualificationCategory, EvaluationCriterion


class Command(BaseCommand):
    help = "Импортирует справочники из CSV-файлов в папке apps/lookups/data/"

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.BASE_DIR, "apps", "lookups", "data")

        self.import_branches(os.path.join(base_dir, "branches.csv"))
        self.import_directions(os.path.join(base_dir, "directions.csv"))
        self.import_categories(os.path.join(base_dir, "categories.csv"))
        self.import_criteria(os.path.join(base_dir, "criteria.csv"))

        self.stdout.write(self.style.SUCCESS("Импорт завершён успешно."))

    def import_branches(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Branch.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Branch.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    bin=row["bin"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Филиалы загружены."))

    def import_directions(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        CompetitionDirection.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CompetitionDirection.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Направления загружены."))

    def import_categories(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        QualificationCategory.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                QualificationCategory.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Квалификационные категории загружены."))

    def import_criteria(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        EvaluationCriterion.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                EvaluationCriterion.objects.create(
                    code=row["code"],
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    description_ru=row["description_ru"],
                    description_kk=row["description_kk"],
                )
        self.stdout.write(self.style.SUCCESS("✅ Критерии оценки загружены."))
