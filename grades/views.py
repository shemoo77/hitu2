from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from grades.models import GradeSheet, StudentGrade
from courses.models import Course
from accounts.models import Student, Doctor
from grades.serializers import GradeSheetSerializer, StudentGradeSerializer

def is_doctor(user):
    return hasattr(user, 'doctor')


def is_student(user):
    return hasattr(user, 'student')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_grades(request):
    user = request.user

    if is_student(user):
        student = user.student
        grades = StudentGrade.objects.filter(student=student)
        serializer = StudentGradeSerializer(grades, many=True)
        return Response(serializer.data)

    return Response({"detail": "You do not have permission to view grades."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grades_for_course(request, course_id):
    user = request.user

    if not is_doctor(user):
        print("hellooooooooz")
        return Response({"detail": "You do not have access permission."}, status=status.HTTP_403_FORBIDDEN)

    doctor = user.doctor

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    # تحقق إن الدكتور فعلاً هو المسؤول عن المادة
    if course.doctor != doctor:
        return Response({"detail": "You do not have permission to access this course."}, status=status.HTTP_403_FORBIDDEN)

    try:
        grade_sheet = GradeSheet.objects.get(course=course)
    except GradeSheet.DoesNotExist:
        return Response({"detail": "No grade sheet found for this course."}, status=status.HTTP_404_NOT_FOUND)

    serializer = GradeSheetSerializer(grade_sheet)
    return Response(serializer.data)


@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_student_grade(request, student_grade_id):
    user = request.user

    if not is_doctor(user):
        return Response({"detail": "You do not have permission to edit grades."}, status=status.HTTP_403_FORBIDDEN)

    doctor = user.doctor

    try:
        student_grade = StudentGrade.objects.get(id=student_grade_id)
    except StudentGrade.DoesNotExist:
        return Response({"detail": "Student grade not found."}, status=status.HTTP_404_NOT_FOUND)

    if student_grade.grade_sheet.course.doctor != doctor:
        return Response({"detail": "You are not authorized to edit this grade."}, status=status.HTTP_403_FORBIDDEN)

    serializer = StudentGradeSerializer(student_grade, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student_grade(request, student_grade_id):
    user = request.user

    if not is_doctor(user):
        return Response({"detail": "You do not have permission to delete grades."}, status=status.HTTP_403_FORBIDDEN)

    doctor = user.doctor

    try:
        student_grade = StudentGrade.objects.get(id=student_grade_id)
    except StudentGrade.DoesNotExist:
        return Response({"detail": "Student grade not found."}, status=status.HTTP_404_NOT_FOUND)

    if student_grade.grade_sheet.course.doctor != doctor:
        return Response({"detail": "You are not authorized to delete this grade."}, status=status.HTTP_403_FORBIDDEN)

    student_grade.delete()
    return Response({"detail": "Grade deleted successfully."})
