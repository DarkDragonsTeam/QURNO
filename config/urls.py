"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    # Excellent! Here's how URLs work and complete a complete MTV cycle (this time the MTV cycle really ends :)
    # By convention, we split URLs in Django per app. In fact, each app has its own urls.py file.
    # Now, for example, we consider the urls.py file of the blog app for you. This is where we really come across
    # include. You will need to import include next to the path (which was imported above).
    # To complete a proper MTV cycle, we need to include the urls.py file depending on each app. Now, depending on
    # each app, we create an absolute URL that every URL associated with that app must pass. Here we have written
    # blog/, so in the blog/urls.py file we wrote the examples like this: /blog/post/list/
    # We just wrote post/list/ there, but here a blog/prefix is added to indicate which app the URL belongs to, and
    # which section the user views.
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("blog/", include("blog.urls")),
    path("admins/", include("admins.urls")),
    path("", include("pages.urls")),
    
]

# 

handler403 = "pages.views.handler403"
handler404 = "pages.views.handler404"
handler500 = "pages.views.handler500"


# By default, Django doesn't serve media files during development (when DEBUG=True).
# We are adding these settings to enable Django to address and manage media files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
