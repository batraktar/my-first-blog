from django.apps import AppConfig


class AppCinemaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cinema'

    def ready(self):
        import app_cinema.signals
