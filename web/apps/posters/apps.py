from django.apps import AppConfig


class PostersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.posters'

    def ready(self):
        import apps.posters.tasks
