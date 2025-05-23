import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.lookups.models import (
    Branch,
    CompetitionDirection,
    QualificationCategory,
    EvaluationCriterion,
    Region,
    Subject,
    SchoolType,
    SchoolForm,
    Location,
    Position,
    School,
)


class Command(BaseCommand):
    help = "Импортирует справочники из CSV-файлов в папке apps/lookups/data/"

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.BASE_DIR, "apps", "lookups", "data")

        self.import_regions(os.path.join(base_dir, "regions.csv"))
        self.import_branches(os.path.join(base_dir, "branches.csv"))
        self.import_directions(os.path.join(base_dir, "directions.csv"))
        self.import_categories(os.path.join(base_dir, "categories.csv"))
        self.import_criteria(os.path.join(base_dir, "criteria.csv"))
        self.import_subjects(os.path.join(base_dir, "subjects.csv"))
        self.import_school_types(os.path.join(base_dir, "schooltype.csv"))
        self.import_school_forms(os.path.join(base_dir, "schoolform.csv"))
        self.import_locations(os.path.join(base_dir, "location.csv"))
        self.import_positions(os.path.join(base_dir, "positions.csv"))
        self.import_schools(os.path.join(base_dir, "schools.csv"))

        self.stdout.write(self.style.SUCCESS("✅ Импорт завершён успешно."))

        self.stdout.write(self.style.SUCCESS("✅ Импорт завершён успешно."))

    def import_regions(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Region.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Region.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    code=row["code"],
                    external_id=row["external_id"],
                )
        self.stdout.write(self.style.SUCCESS("✅ Регионы загружены."))

    def import_branches(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Branch.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                region = None
                region_code = row.get("region_code")
                if region_code:
                    try:
                        region = Region.objects.get(code=region_code)
                    except Region.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"⚠️ Регион с кодом '{region_code}' не найден."))

                Branch.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    bin=row["bin"],
                    external_id=row["external_id"],
                    region=region
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

    def import_subjects(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Subject.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                Subject.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Предметы загружены."))

    def import_school_types(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        SchoolType.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                SchoolType.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Типы школ загружены."))

    def import_school_forms(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        SchoolForm.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                SchoolForm.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Формы школ загружены."))

    def import_locations(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Location.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                Location.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Локации загружены."))

    def import_positions(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        Position.objects.all().delete()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                Position.objects.create(
                    name_ru=row["name_ru"],
                    name_kk=row["name_kk"],
                    external_id=row["external_id"]
                )
        self.stdout.write(self.style.SUCCESS("✅ Должности загружены."))

    def import_schools(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(f"Пропущено: {filepath} не найден")
            return

        School.objects.all().delete()

        # Загружаем справочники в память
        region_map = {str(r.external_id): r for r in Region.objects.all()}
        location_map = {str(l.external_id): l for l in Location.objects.all()}
        school_type_map = {str(t.external_id): t for t in SchoolType.objects.all()}
        school_form_map = {str(f.external_id): f for f in SchoolForm.objects.all()}

        def resolve(map_, key):
            key = key.strip()
            return map_.get(key) if key.isdigit() else None

        schools = []

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                region = resolve(region_map, row["region"])
                location = resolve(location_map, row["location"])
                school_type = resolve(school_type_map, row["schooltype"])
                school_form = resolve(school_form_map, row["schoolform"])

                school = School(
                    name_ru=row["name_ru"].strip(),
                    name_kk=row["name_kk"].strip(),
                    region=region,
                    location=location,
                    school_type=school_type,
                    school_form=school_form,
                    external_id=int(row["external_id"]),
                )
                schools.append(school)

        School.objects.bulk_create(schools, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"✅ Загружено школ: {len(schools)}"))
