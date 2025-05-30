from rest_framework import serializers
from accounts.models import Student
from django.contrib.auth.models import User
from .models import Announcement

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    image = serializers.SerializerMethodField()  # هنجيب الصورة يدويًا

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'email', 'name', 'mobile', 'national_id', 'structure', 'image']

    def get_image(self, obj):
        try:
            return obj.dash.image.url if obj.dash.image else None
        except:
            return None

############################################################################


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']
