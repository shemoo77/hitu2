from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Student
from .models import Course, StudentCourse

# لما طالب يتضاف أو يتعدل
@receiver(post_save, sender=Student)
def assign_courses_to_student(sender, instance, created, **kwargs):
    student = instance
    if not student.structure:
        return

    courses = Course.objects.filter(
        department=student.structure.department,
        academic_year=student.structure.year,
        semester=student.structure.semester
    )

    for course in courses:
        StudentCourse.objects.get_or_create(student=student, course=course)


# لما مادة تتضاف أو تتعدل
@receiver(post_save, sender=Course)
def assign_course_to_students(sender, instance, created, **kwargs):
    course = instance

    students = Student.objects.filter(
        structure__department=course.department,
        structure__year=course.academic_year,
        structure__semester=course.semester
    )

    for student in students:
        StudentCourse.objects.get_or_create(student=student, course=course)
