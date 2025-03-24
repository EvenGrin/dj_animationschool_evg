from django.apps import AppConfig


class AnimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anim_app'

    def ready(self):
        import anim_app.signals
