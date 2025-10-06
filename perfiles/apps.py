from django.apps import AppConfig

class PerfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "perfiles"

    def ready(self):
        from . import signals  #registra los signals
