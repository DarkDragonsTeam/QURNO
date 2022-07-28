from django import forms

from django.contrib.auth import get_user_model

# Create your custom forms here.


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            "avatar",
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
        )
