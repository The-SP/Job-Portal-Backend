from django.apps import AppConfig


class UserSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_system"

    def ready(self):
        import user_system.signals