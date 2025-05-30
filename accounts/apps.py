# apps.py داخل accounts
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # تأكد من استيراد السيجنال
