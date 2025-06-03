from rest_framework import serializers
from grades.models import GradeSheet, StudentGrade

class StudentGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='grade_sheet.course.name', read_only=True)
    percentage = serializers.FloatField(read_only=True)
    letter_grade = serializers.CharField(read_only=True)
    total_score = serializers.FloatField(read_only=True)

    class Meta:
        model = StudentGrade
        fields = [
            'student_name',
            'course_name',
            'midterm_score',
            'section_exam_score',
            'final_exam_score',
            'year_work_score',
            'total_score',
            'percentage',
            'letter_grade'
        ]

    def validate(self, data):
        # نجيب الدرجات اللي اتدخلت
        midterm = data.get('midterm_score', self.instance.midterm_score if self.instance else 0)
        section = data.get('section_exam_score', self.instance.section_exam_score if self.instance else 0)
        final = data.get('final_exam_score', self.instance.final_exam_score if self.instance else 0)
        year_work = data.get('year_work_score', self.instance.year_work_score if self.instance else 0)

        total = midterm + section + final + year_work

        # نجيب الفول سكور من grade_sheet
        grade_sheet = self.instance.grade_sheet if self.instance else self.initial_data.get('grade_sheet')
        if not grade_sheet:
            raise serializers.ValidationError("يجب تحديد ورقة الدرجات (grade sheet)")

        # لو جاي id بدل object
        if isinstance(grade_sheet, int):
            try:
                from grades.models import GradeSheet
                grade_sheet = GradeSheet.objects.get(pk=grade_sheet)
            except GradeSheet.DoesNotExist:
                raise serializers.ValidationError("Grade sheet غير موجود")

        full_score = grade_sheet.full_score or 100

        if total > full_score:
            raise serializers.ValidationError(
                f"إجمالي الدرجات ({total}) لا يمكن أن يتجاوز الدرجة النهائية للمادة ({full_score})"
            )

        return data


class GradeSheetSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_grades = StudentGradeSerializer(many=True, read_only=True)

    class Meta:
        model = GradeSheet
        fields = ['course', 'course_name', 'full_score', 'student_grades']
