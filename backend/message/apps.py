from django.apps import AppConfig


class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.message'

    def ready(self):
        import backend.message.signals
