from django.apps import AppConfig

class GradesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grades'

    def ready(self):
        import grades.signals  # دا بيشغل السيجنال أول ما الأبلكيشن يشتغل
