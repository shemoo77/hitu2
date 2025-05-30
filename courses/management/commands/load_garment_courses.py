from django.core.management.base import BaseCommand
import json
from courses.models import Course
from structure.models import DepartmentChoices, AcademicYearChoices, SemesterChoices


def map_academic_year(year_key):
    return {
        'year_1': AcademicYearChoices.FIRST,
        'year_2': AcademicYearChoices.SECOND,
        'year_3': AcademicYearChoices.THIRD,
        'year_4': AcademicYearChoices.FOURTH,
    }.get(year_key)


def map_semester(term_key):
    return {
        'term_1': SemesterChoices.FIRST,
        'term_2': SemesterChoices.SECOND,
    }.get(term_key)


class Command(BaseCommand):
    help = 'Reload Garment Technology department courses from JSON (clear old and add new)'

    def handle(self, *args, **kwargs):
        json_path = 'data/garment_courses.json'  # عدلي المسار لو الملف في مكان تاني
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ File not found: {json_path}"))
            return

        garment_courses = data.get('garment_technology', {})

        # Delete old Garment Technology courses
        deleted, _ = Course.objects.filter(department=DepartmentChoices.GARMENT_MANUFACTURING).delete()
        self.stdout.write(self.style.WARNING(f"🗑️ Deleted {deleted} old courses from Garment Technology department"))

        count = 0
        for year_key, year_data in garment_courses.items():
            academic_year = map_academic_year(year_key)

            for term_key, courses in year_data.items():
                semester = map_semester(term_key)

                if not academic_year or not semester:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ Invalid academic year or semester: {year_key}, {term_key}"
                    ))
                    continue

                for name in courses:
                    Course.objects.create(
                        name=name,
                        department=DepartmentChoices.GARMENT_MANUFACTURING,
                        academic_year=academic_year,
                        semester=semester
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully added {count} new courses for Garment Technology department"))
