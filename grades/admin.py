from django.contrib import admin
from .models import GradeSheet, StudentGrade


# عرض الدرجات داخل كل GradeSheet
class StudentGradeInline(admin.TabularInline):
    model = StudentGrade
    extra = 0  # ميظهرش صفوف فاضية
    readonly_fields = ('percentage', 'letter_grade')  # مش عايزة تتعدل من الأدمن


# عرض كشف الدرجات (GradeSheet)
@admin.register(GradeSheet)
class GradeSheetAdmin(admin.ModelAdmin):
    list_display = ('course',)
    inlines = [StudentGradeInline]


# لو عايزة تعرضي StudentGrade لوحدها كمان
@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'grade_sheet', 'midterm_score', 'section_exam_score', 'final_exam_score', 'year_work_score', 'total_score', 'percentage', 'letter_grade')
    readonly_fields = ('percentage', 'letter_grade')
    list_filter = ('grade_sheet__course',)
    search_fields = ('student__name', 'grade_sheet__course__name')
