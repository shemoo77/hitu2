import random
import qrcode
import os
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import QRCodeSession
from courses.models import Course
from django.utils import timezone
import json

def qr_generation_page(request, course_id):
    return render(request, 'generate_qr_live.html', {'course_id': course_id})

def generate_qr_code_ajax(request, course_id):
    course = Course.objects.get(id=course_id)
    random_number = random.randint(1000, 9999)
    qr_code_data = f"{random_number}"  # بس الرقم علشان الطالب يستخدمه

    qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_codes_dir, exist_ok=True)

    filename = f"qr_code_{int(datetime.now().timestamp())}.png"
    file_path = os.path.join(qr_codes_dir, filename)

    qr = qrcode.make(qr_code_data)
    qr.save(file_path)

    qr_session = QRCodeSession.objects.create(
        course=course,
        code=random_number,
        image=f'qr_codes/{filename}',
        is_active=True  # مهم علشان الـ IntegrityError اللي حصل قبل كده
    )

    image_url = f"{settings.MEDIA_URL}qr_codes/{filename}"
    return JsonResponse({'image_url': image_url})

#########################################################################

def student_attendance_page(request):
    return render(request, 'student_attendance.html')

def verify_qr_code(request):
    code = request.GET.get('qr_code_data')
    try:
        qr_session = QRCodeSession.objects.get(
            code=code,
            is_active=True,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        )


        time_elapsed = timezone.now() - qr_session.created_at
        if time_elapsed > timedelta(minutes=1):
            return JsonResponse({'status': 'error', 'message': 'QR Code منتهي الصلاحية'})

        return JsonResponse({'status': 'success', 'message': 'QR Code سليم'})

    except QRCodeSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'QR Code غير صالح'})
    
#############################################################################

def verify_location(request):
    data = json.loads(request.body)
    lat = float(data.get("latitude"))
    lon = float(data.get("longitude"))

    correct_lat = 30.0444
    correct_lon = 31.2357
    allowed_distance = 0.01

    if abs(lat - correct_lat) <= allowed_distance and abs(lon - correct_lon) <= allowed_distance:
        return JsonResponse({'status': 'success', 'message': 'الموقع صحيح'})
    else:
        return JsonResponse({'status': 'error', 'message': 'أنت مش في الموقع المسموح 😢'})
