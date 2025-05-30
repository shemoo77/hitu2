from django.urls import path
from grades import views

urlpatterns = [
    path('mygrades/', views.my_grades, name='my_grades'),
    # لعرض درجات الطالب نفسه (قراءة فقط)

    path('course/<int:course_id>/grades/', views.grades_for_course, name='grades_for_course'),
    # الدكتور بيشوف كشف درجات مادة معينة

    path('student-grade/<int:student_grade_id>/update/', views.update_student_grade, name='update_student_grade'),
    # الدكتور بيعدل أو يضيف درجة طالب (PATCH أو PUT أو POST)

    path('student-grade/<int:student_grade_id>/delete/', views.delete_student_grade, name='delete_student_grade'),
    # الدكتور بيحذف درجة طالب
]
