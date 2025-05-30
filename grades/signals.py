from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import StudentCourse
from grades.models import GradeSheet, StudentGrade

@receiver(post_save, sender=StudentCourse)
@receiver(post_save, sender=StudentCourse)
def add_student_to_gradesheet(sender, instance, created, **kwargs):
    if not created:
        return

    student = instance.student
    course = instance.course

    grade_sheet, _ = GradeSheet.objects.get_or_create(course=course)

    exists = StudentGrade.objects.filter(grade_sheet=grade_sheet, student=student).exists()
    if not exists:
        StudentGrade.objects.create(
            grade_sheet=grade_sheet,
            student=student,
            score=0  # الدرجة الافتراضية
        )
