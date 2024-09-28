from django.apps import AppConfig


class CounterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'counter'


    def ready(self):
        import counter.signals  # Import the signals module