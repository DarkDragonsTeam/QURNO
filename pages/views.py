from django.shortcuts import render
from django.utils import timezone

from taggit.models import Tag

from blog.models import Post, Category

# Create your views here.

global tags_list
tags_list = Tag.objects.all()

global categories_list
categories_list = Category.objects.filter(active=True)


def handler403(request, *args, **argv):
    context = {"tags_list": tags_list, 
               "categories": categories_list}
    return render(request, "403.html", context)


def handler404(request, *args, **argv):
    context = {"tags_list": tags_list, 
               "categories": categories_list}
    return render(request, "404.html", context)


def handler500(request, *args, **argv):
    context = {"tags_list": tags_list, 
               "categories": categories_list}
    return render(request, "500.html", context)


def index_page_view(request):
    recent_posts = Post.objects.filter(active=True).exclude(status="0").filter(category__active=True)\
        .filter(pub_datetime__lte=timezone.now()).filter(pub_datetime__lt=timezone.now())\
            .order_by("-pub_datetime")[0:6]
    
    context = {
        "tags_list": tags_list,
        "categories": categories_list,
        "recent_posts": recent_posts,
    }
    return render(request, "pages/index.html", context)


def about_page_view(request):
    
    return render(request, "pages/about.html", {"tags_list": tags_list, "categories": categories_list})
