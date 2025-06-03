# grades/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Student, Doctor
from courses.models import Course

class GradeSheet(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    full_score = models.FloatField(default=100)  # الدكتور يحدد الدرجة النهائية للمادة

    def __str__(self):
        return f"Grade Sheet for {self.course.name}"

class StudentGrade(models.Model):
    grade_sheet = models.ForeignKey(GradeSheet, on_delete=models.CASCADE, related_name='student_grades')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    midterm_score = models.FloatField(default=0)
    section_exam_score = models.FloatField(default=0)
    final_exam_score = models.FloatField(default=0)
    year_work_score = models.FloatField(default=0)

    total_score = models.FloatField(default=0)  # مجموع كل الدرجات
    percentage = models.FloatField(default=0)
    letter_grade = models.CharField(max_length=2, blank=True)

    class Meta:
        unique_together = ('grade_sheet', 'student')

    def __str__(self):
        return f"{self.student} - {self.total_score}"

    def clean(self):
        # جمع الدرجات
        total = (
            self.midterm_score +
            self.section_exam_score +
            self.final_exam_score +
            self.year_work_score
        )

        if self.grade_sheet and total > self.grade_sheet.full_score:
            raise ValidationError(
                f"إجمالي الدرجات ({total}) لا يمكن أن يتجاوز الدرجة النهائية ({self.grade_sheet.full_score})"
            )

    def save(self, *args, **kwargs):
        # أول حاجة نفذ الفاليديشن
        self.full_clean()

        # احسب التوتال
        self.total_score = (
            self.midterm_score +
            self.section_exam_score +
            self.final_exam_score +
            self.year_work_score
        )

        full_score = self.grade_sheet.full_score or 100
        if full_score > 0:
            self.percentage = round((self.total_score / full_score) * 100, 2)
        else:
            self.percentage = 0

        # التقدير بالحروف
        if self.percentage >= 97:
            self.letter_grade = "A+"
        elif self.percentage >= 93:
            self.letter_grade = "A"
        elif self.percentage >= 89:
            self.letter_grade = "A-"
        elif self.percentage >= 84:
            self.letter_grade = "B+"
        elif self.percentage >= 80:
            self.letter_grade = "B"
        elif self.percentage >= 76:
            self.letter_grade = "B-"
        elif self.percentage >= 73:
            self.letter_grade = "C+"
        elif self.percentage >= 70:
            self.letter_grade = "C"
        elif self.percentage >= 67:
            self.letter_grade = "C-"
        elif self.percentage >= 64:
            self.letter_grade = "D+"
        elif self.percentage >= 60:
            self.letter_grade = "D"
        else:
            self.letter_grade = "F"

        super().save(*args, **kwargs)


# SIGNAL عشان لما يتغير full_score يعيد حساب النسب لكل الطلاب
@receiver(post_save, sender=GradeSheet)
def update_student_grades_percentage(sender, instance, **kwargs):
    for student_grade in instance.student_grades.all():
        student_grade.save()
