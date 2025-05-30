from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Student
from .models import Dash
from .Serializer import StudentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def personal_info(request):
    try:
        student = Student.objects.get(user=request.user)

        # لو الطلب GET: نرجع البيانات
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)

        # لو الطلب POST: نرفع الصورة
        elif request.method == 'POST':
            dash, created = Dash.objects.get_or_create(student=student)
            dash.image = request.FILES.get('image')
            dash.save()
            return Response({'message': 'Image uploaded successfully'})

    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

# @login_required # static 
# def personal_info_page(request):
#     student = Student.objects.get(user=request.user)
#     return render(request, 'personal_info.html', {'student': student})

#################################################################################

# dashboard/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Announcement
from .Serializer import AnnouncementSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcement_api(request):
    # 1. الطالب بيطلب يشوف الإعلانات
    if request.method == 'GET':
        announcements = Announcement.objects.all().order_by('-created_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

    # 2. الدكتور بيضيف إعلان جديد
    elif request.method == 'POST':
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # 3. الدكتور بيعدل إعلان
    elif request.method == 'PUT':
        announcement_id = request.data.get('id')
        announcement = get_object_or_404(Announcement, id=announcement_id, created_by=request.user)
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 4. الدكتور بيحذف إعلان
    elif request.method == 'DELETE':
        announcement_id = request.data.get('id')
        announcement = get_object_or_404(Announcement, id=announcement_id, created_by=request.user)
        announcement.delete()
        return Response({'message': 'Deleted successfully.'})
