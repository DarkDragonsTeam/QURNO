from django.urls import path

from . import views

# Create your custom urls here.

app_name = "pages"

urlpatterns = [
    path("", views.index_page_view, name="index"),
    path("about/", views.about_page_view, name="about"),
]
