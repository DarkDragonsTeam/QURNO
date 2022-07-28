from django.urls import path

from . import views

# Create your custom views here.


app_name = "admins"


urlpatterns = [
    path("", views.admin_portal_view, name="admins"),
    path("profile/", views.admin_profile_view, name="profile"),
    path("terms/", views.admin_terms_view, name="terms"),

    path("blog/post/list/", views.post_list_view_lazy, name="post_list_lazy"),
    path("blog/post/list/page/", views.post_list_view, name="post_list"),
    path("blog/post/search/list/", views.searched_post_list_view, name="post_search"),
    path("blog/post/list/author/<str:author_username>/", views.post_list_view, name="post_list"),
    path("blog/post/detail/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("blog/post/create/", views.post_create_view, name="post_create"),
    path("blog/post/update/<int:pk>/", views.post_update_view, name="post_update"),
    path("blog/post/delete/<int:pk>/", views.post_delete_view, name="post_delete"),
    path("blog/category/list/", views.category_list_view_lazy, name="category_list_lazy"),
    path("blog/category/list/page/", views.category_list_view, name="category_list"),
    path("blog/category/list/author/<str:category_designer_username>/", views.category_list_view, name="category_list"),
    path("blog/category/detail/<int:pk>/", views.category_detail_view, name="category_detail"),
    path("blog/category/create/", views.category_create_view, name="category_create"),
    path("blog/category/update/<int:pk>/", views.category_update_view, name="category_update"),
    path("blog/category/delete/<int:pk>/", views.category_delete_view, name="category_delete"),
]
