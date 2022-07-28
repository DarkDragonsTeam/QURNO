from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.fields import Textarea as TextareaField
from django.forms.widgets import Textarea

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from .models import Post, Category

# Create your custom forms here.


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['pub_datetime'] = JalaliDateField(label=_('date'),
            widget=AdminJalaliDateWidget
        )

        self.fields['pub_datetime'] = SplitJalaliDateTimeField(label=_('date time'),
            widget=AdminSplitJalaliDateTime
        )

    class Meta:
        model = Post
        fields = ("banner",
                  "title",
                  "content",
                  "description",
                  "slug",
                  "pub_datetime",
                  "category",
                  "tags",
                  "read_time",
                  "status",
                  "active",
                  )


class MiniPostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "description",
            "slug",
            "category",
            "tags",
        )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            "title",
            "description",
            "slug",
            "active",
        )
        
        
class PostSearchForm(forms.Form):
    query = forms.CharField(max_length=225)
