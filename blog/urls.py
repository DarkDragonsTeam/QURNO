""""
This is (almost) the end of the MTV cycle. Why? So far we have created a Template, a Model, a View and a Sequential
View, but Template alone does not mean HTML files. Here we consider both Template and Pattern logic to be synonymous.
In fact, we have to fix the addresses. last shot:)

Here you will learn more about including or include logic. As you've probably seen before, this logic comes from the
PHP programming language. We will explain more about this. include means to receive a thing, part or section, without
the slightest change. In fact, when you use include, what is included is just rewritten.

We import the required modules. The first module for designing a URL is the path. path allows us several useful tasks,
we need 3 of them in the relatively preliminary stage. path takes an address from you, path addresses always have a
specific format, you will definitely get in trouble if you go out of their specific format. Its format can be seen in
the following examples. The second input of the path is a view, we have seen many times that the path is sensitive to
the type of views! Make sure the path is not sensitive to the type of views, you just need to be aware of its use. We
have called the view (in this app) as FBVs. An example of this can be seen below. The third entry is the name of this
URL. URLs are very important, set them. We will certainly face them later.
"""

from django.urls import path, re_path

# To display a view, we must import it from the views.py file.
from . import views

# Create your custom urls here.

# You may be wondering what this app_name means? app_name is a kind of security lock that further increases the
# accuracy of our work. When we use URLs, we deal with it (especially in templates).
app_name = "blog"

# Here is the part that includes. In fact, the list of URLs is located in this file. Django does not recognize this list
# by default, we just designed it to use in the config/urls.py file.
urlpatterns = [
    # This is a trivial example of URLs. In fact, in most cases you do not need this path and post_list_lazy, we have
    # already said that this function is made just to sort URLs. This is an example of how when a user enters
    # /blog/post/list/, they enter a more accurate address to make the Pagination System work properly.
    path("post/list/", views._post_list_view_lazy, name="post_list_lazy"),

    # But this is a real example of a View/Template. As you can see, we created a complete view called post_list_view
    # in the views.py file; We call it here and use it properly. In fact, we now have an address like this:
    # 127.0.0.1:port|localhost:port|host:port|blog/post/list/view/page/
    # But where is the host/blog/ ? You can enter the config/urls.py file here.
    path("post/list/page/", views.post_list_view, name="post_list"),
    
    path("post/search/list/", views.searched_post_list_view, name="post_search"),
    
    # These are some types of url addresses that contain loads of information. In fact, they refer an input to View
    # functions. Interestingly, for example we have reclaimed a post_author, or a tag_slug. We have checked to change
    # the posts variable. We change these variables depending on the URLs. Here you can see some types of sending
    # variables to functions (or classes).
    # /<type:function_argument_name>/
    re_path(r"post/list/tag/(?P<tag_slug>[-\w]+)/", views.post_list_view, name="post_list"),
    path("post/list/author/<str:author_username>/", views.author_post_list_view, name="author_post_list"),
    # In this section, you will notice that a slug is filled in urls.py. In fact, the user calls a specific slug through
    # urls.py, and we get it through post_detail_view.
    re_path(r"post/detail/(?P<slug>[-\w]+)/", views.post_detail_view, name="post_detail"),
    
    path("category/list/", views.category_list_view, name="category_list"),
    re_path(r"category/detail/(?P<slug>[-\w]+)/", views.category_detail_view, name="category_detail"),
    
    path("tag/list/", views.tag_list_view, name="tag_list"),
]
