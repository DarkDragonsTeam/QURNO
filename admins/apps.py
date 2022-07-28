from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _

class AdminsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admins'
    
    # Persian format settings
    verbose_name = _("حساب ها")
