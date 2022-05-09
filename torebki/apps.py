from django.apps import AppConfig


class TorebkiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'torebki'

    def ready(self):
        import torebki.signals
