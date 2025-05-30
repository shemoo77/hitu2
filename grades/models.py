# grades/models.py
from django.db import models
from accounts.models import Student , Doctor
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
    score = models.FloatField(default=0)  # الدرجة العادية
    percentage = models.FloatField(default=0)  # تتحسب تلقائي
    letter_grade = models.CharField(max_length=2, blank=True)  # تتحسب تلقائي

    class Meta:
        unique_together = ('grade_sheet', 'student')

    def __str__(self):
        return f"{self.student} - {self.score}"

    def save(self, *args, **kwargs):
        full_score = self.grade_sheet.full_score or 100
        if full_score > 0:
            self.percentage = (self.score / full_score) * 100
        else:
            self.percentage = 0

        # نحسب التقدير بالحروف
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
