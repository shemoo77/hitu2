from django.contrib import admin
from .models import Course, StudentCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'academic_year', 'semester', 'doctor')  # الأعمدة اللي تظهر في القائمة
    list_filter = ('department', 'academic_year', 'semester')  # فلاتر على الجنب لتنقية حسب القسم والسنة والترم
    search_fields = ('name',)  # خانة بحث باسم المادة
    ordering = ('department', 'academic_year', 'semester')  # ترتيب العرض

    fieldsets = (
        ('معلومات المادة', {
            'fields': ('name', 'department', 'academic_year', 'semester', 'doctor', 'drive_link')
        }),
    )


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    search_fields = ('student__name', 'course__name')
    list_filter = ('course__department', 'course__academic_year', 'course__semester')
