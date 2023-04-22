from django.apps import AppConfig
from django.conf import settings
class MonthreportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monthReport'

    def ready(self):
        from .jobs import updater

        if settings.SCHEDULER_DEFAULT: # 한 번만 실행 
            updater.start()