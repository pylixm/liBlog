from django.apps import AppConfig


class VisitorConfig(AppConfig):
    name = 'liBlog.visitor'
    verbose_name = "Visitor"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
