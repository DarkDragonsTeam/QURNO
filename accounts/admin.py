from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    This model helps you to fully customize your model for the admin panel and optimize it to be displayed in the
    admin panel in the best possible way.

    To better understand this section, it is recommended that you learn more about Django Admin and do some research
    on it.
    """

    # We must first rewrite what forms and models the admin panel uses.
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Then we set what the admin panel user interface looks like. For example, what to show in a sample, what to
    # live edit, and what to show in admin panel searches.
    list_display = ("get_avatar_thumbnail", "username", "first_name", "last_name", "is_staff", "is_author", )
    search_fields = ("username", "first_name", "last_name", "email", )
    list_filter = ("is_superuser", "is_staff", "is_author", "date_joined", )

    # Then we need to configure the admin panel fields and add fieldset. To understand this part, be sure to refer
    # to the Django Project documents.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("avatar", "first_name", "last_name", "email", "bio", "is_author", ), }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("avatar", "bio", "is_author"), }),
    )


# Models that you register in the admin panel:
admin.site.register(CustomUser, CustomUserAdmin)
