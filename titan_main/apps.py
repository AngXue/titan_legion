from django.apps import AppConfig


class TitanEsiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'titan_main'

    def ready(self):
        import titan_main.signals
