from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

# Create your custom forms here.


class CustomUserCreationForm(UserCreationForm):
    """
    In this class you will design the structure of the CustomUser model forms.
    In fact, this structure (class) helps you to design and customize a custom form for your new model (CustomUser)
    and use it throughout the project.

    You can change or add the required fields structure here.
    """

    class Meta:
        # Here we set the main settings of the model.

        model = CustomUser
        fields = ("avatar", "first_name", "last_name", "username", "email", "bio", )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
