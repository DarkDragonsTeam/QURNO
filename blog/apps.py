from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # Here we adjust the additional translation settings. In fact, we introduce the Persian version (in Persian format)
    # of the app to Django.
    verbose_name = _("بلاگ")
