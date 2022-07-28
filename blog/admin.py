from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Category, Post, Comment

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    """
    This class was created to manage the appearance of the Category model in the admin panel. You can customize this
    class far beyond what we have created, with different fields and commands (and, of course, as already mentioned,
    familiarity with the Django admin panel).
    """

    list_display = ("title", "active", )
    list_editable = ("active", )
    list_filter = ("datetime_created", "datetime_modified", "active", )
    search_fields = ("title", "description", )


# This is the essence of the matter. Here we register the decorations we made in Django Admin Panel.
admin.site.register(Category, CategoryAdmin)


# This is another way to register information and models in the Django admin panel.
@admin.register(Post)
class PostAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    exclude = ("views", )

    list_display = ("get_banner_thumbnail", "title", "get_pub_datetime_jalali_date", "author", "status", "active", )
    list_filter = ("active", "author", "pub_datetime", "datetime_created", "datetime_modified", )
    search_fields = ("title", "content", "author", "message", )
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "get_text_thumbnail", "active")
    list_editable = ("active", )
    search_fields = ("author", "title", "text", )
    list_filter = ("datetime_created", "datetime_modified", "active", )
