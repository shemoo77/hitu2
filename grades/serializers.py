from rest_framework import serializers
from grades.models import GradeSheet, StudentGrade

class StudentGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='grade_sheet.course.name', read_only=True)  # جلب اسم المادة
    percentage = serializers.FloatField(read_only=True)
    letter_grade = serializers.CharField(read_only=True)

    class Meta:
        model = StudentGrade
        fields = ['student_name', 'course_name', 'score', 'percentage', 'letter_grade']

class GradeSheetSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_grades = StudentGradeSerializer(many=True, read_only=True)

    class Meta:
        model = GradeSheet
        fields = ['course', 'course_name', 'student_grades']
