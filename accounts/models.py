from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils.html import format_html

# Create your models here.


class CustomUser(AbstractUser):
    """
    This class manages our users. In fact, every user is an instance of this class, at least this is Django architecture
    Django Authentication System is directly related to this class, and so is your database. This class is very
    important both in terms of security and user experience.

    Now it's time to realize that this system has already been designed! Yes! Django has already designed this system.
    It is enough for us to change it. The easiest style to change is to add two different fields. You can rewrite and
    distribute a variety of behaviors (methods) in this class, including the login system.

    Django has an internal model of this class, but since it is better not to manipulate Django internal resources, we
    will build this class to make the database dependent on this model.
    In fact, we do not want Django to use its internal model for user instances, so we are building this class.
    You are free to type the pass value at the bottom line to preserve the original Django model, just attach the
    database to this model so that we will not have a problem later if we need a change in the User class.
    """
    
    # Override Vars and Methods:
    email = models.EmailField(_("ایمیل"), max_length=225, null=True, blank=True, unique=True)

    # For example, we will add two fields to the default Django model to give you an example. Avatar field and bio
    # field, which are responsible for saving the avatar image and the biography of the User Instance.

    avatar = models.ImageField(_("آواتار"), upload_to="accounts/", default="defaults/user_default_avatar.png",
                               blank=True)
    bio = models.TextField(_("بیوگرافی"), null=True, blank=True)
    is_author = models.BooleanField(_("وضعیت نویسندگی"), default=False, null=False, blank=False)

    # You have already seen a lot about this type of method. For details, visit the models.py page in the blog
    # directory.
    def get_avatar_thumbnail(self):
        return format_html("""
        <span>
            <img src="{}" style="height: 50px; width: 50px; border-radius: 50%;">
        </span>
        """.format(self.avatar.url))
    get_avatar_thumbnail.short_description = _("آواتار")

    class Meta:
        # Persian format settings of this model
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربر ها")
