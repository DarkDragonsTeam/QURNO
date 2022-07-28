from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from taggit.models import Tag
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post, Category
from .forms import PostSearchForm

# Create your views here.

tags_list = Tag.objects.all()[0:25]

categories_list = Category.objects.filter(active=True)[0:25]


def _post_list_view_lazy(request):
    """
    As the name implies, this function has no special function, you do not need to be too involved in this function.
    This function is only for organizing URLs and paginator/pagination topic in Django. The type of paginator used
    in this project is a bit more specific and complex than regular Paginator, so it needs this function to sort the
    addresses of the loads.

    This function returns a fake HTTP request that prevents the PageNotAnInteger error in the Paginator System. In fact,
    the Paginator System used in this project always requires a number in the URL Query.

    Reminder: /URL/ADDRESS/?page=X

    When the user requests the main function (post_list_view), he naturally does not enter a specific number [can be
    seen in the urls.py file]. We set that if the user did not enter a specific number, it will automatically return
    "?page=1" with a delay (or, as the saying goes, lazy :) so that the Paginator System does not encounter a
    PageNotAnInteger error.
    """
    return HttpResponseRedirect("/blog/post/list/page/")


def post_list_view(request, tag_slug=None):
    """
    Here we enter the main part of the View section in Django. It is good to know that there are two types of View
    in Django, Functional Based Views, and Class Based View (which stands for FBVs and CBVs. These principles are not
    originally related to Django and are common in MVC and MTV architecture.) Now we Which to choose? What are the
    differences between these two types of views? There are many differences between the two methods, and they cannot
    be explained in one comment. But in general, CBVs make things shorter. We will definitely try to show you examples
    of it later. CBVs are classes inherited from views. generic in Django and include a world of different methods and
    variables that have already been prepared. But FBVs are structured functions that you start from scratch with a
    request variable (which is also filled in by Django's own [MVC] architecture).

    FBVs are more accurate, lighter, and faster, but CBVs are heavier and contain more information, and certainly have
    more prefabricated features. Preliminary (and somewhat advanced) work is much easier with CBVs. But "in our opinion"
    working with FBVs is somewhat more advanced and accurate. In fact, when you start building something from scratch,
    you become more aware of the logic and meaning of what you have done. However, you can also read the resources on
    CBVs to learn a lot about the logic of their work.

    We want to know more about the views and the logic of their work. Views are structures that form the back-end of a
    template. They set what works (how) and is displayed. Templates are actually Hard Code, and do not contain any
    specific content, but views are by definition lively and can exhibit dynamic behaviors. Views depend on Models.
    All queries and query systems in MVC and MTV must be done in Models. Views request, fetch, and display the result
    from the database (via models).

    This is the whole logic of View work in a nutshell :)
    """
    tag = None
    current_posts_author = None

    # Well, excellent. Now it's time to learn how to query in Django. Queries in Django (and MVC and MTV architectures)
    # are usually done with database managers. A manager has the task of fetching a batch of information from the
    # database in a categorized and orderly manner. A manager that is present in all Models by default is "objects".
    # object Provides you with all the database information.
    # You might have expected us to import SQL queries now, but you were wrong! We use the ORM system in Django by
    # default. One important point is that you should be aware of SQL injection when using raw SQL, but Django ORM fixes
    # this problem by default! Isn't that great?
    # Unfortunately, Django ORM is not something that can be taught in the comments. Needs a lot of study. But if you
    # read the codes and queries (for example the following queries) carefully, you will definitely get acquainted with
    # the query process in Django ORM.
    posts = Post.objects.all().filter(active=True).exclude(status="0").filter(category__active=True)\
        .filter(pub_datetime__lte=timezone.now()).filter(pub_datetime__lt=timezone.now())
    
    # We reached some interesting parts of the project. It's time to add some detail to the tagging system.
    # Many parts of the tagging system are missing in django-taggit. In fact, the lack of slugs is felt in taggit with
    # Persian/Arabic format, but we prefer that this is a bug in QURNO and you fix it :)
    # We have put a value of tag_slug equal to the default value of None in the entries of the post_list_view function,
    # which makes us allow this variable to be empty, but why is this variable needed?
    if tag_slug:
        # Here we will check if the user has called a tag or not, and we will repeat the same process.
        try:
            tag = Tag.objects.get(slug=tag_slug)
        except ObjectDoesNotExist:
            raise Http404

        # Here too, we add a filter to the value of the previous posts to filter the posts that have the tag that the
        # user called.
        posts = posts.filter(tags__in=(tag, ))

    # The next part is the "pagination" system.
    # We'd sure you have seen the Pagination System load on various sites, oh! When you were playing a blog site, the
    # bottom of the page was a button that showed you several pages, you could go to the page, each page had equal post
    # layout, remember? There is another site :))))))))))) This system is called paging (Pagination) system.

    # Here we create an object of Paginator class in Django, this object allows us to start initialization for a
    # ListView that merges with Pagination.
    # This object takes two primary inputs, the first input is the query you want (which should be of the ListView type)
    # and the second input is the number of queries (pagination) per page. In fact, the second value is a divider that
    # divides the query into pages and sections for the number you assign to it.
    paginator = Paginator(posts, 25)

    # Here is an interesting part of Django where you will learn more about the request variable. This variable has
    # many uses that make you use it more and more. At request, most of what we do is get the URL from the user.
    # When you Pagination, it will add a "?page=X[number]" value to your URL (Response), which will let the
    # (Controllers) in Django know where we are located on the Pagination.
    page_number = request.GET.get("page")

    # Here is the part where Paginator is enabled. In fact, the Paginator class is responsive to a particular number,
    # and until it receives that number, it can be said that it is almost not activated.
    # We have enabled Paginator in another variable, and the required number (described above) is stored in the
    # page_number variable, so we can easily pass it to the new variable.
    page_obj = paginator.get_page(page_number)

    # In normal Paginator, there is no need for this section. But we do not make a normal Paginator! We want to
    # design a beautiful and detailed Paginator. To design this Paginator, we need to enable the following value.
    # Understanding this value requires study, but it briefly says to display pages one through three, and leave the
    # rest to the last page and one to the end ..., and as long as the user moves the numbers forward, forward Go and
    # show more numbers. We will face this issue more in the templates.
    # You may be wondering what "page_number or 1" means at the bottom line? This is a tiny Python technique that
    # allows you to enter the first page of Pagination instead of PageNotAnInteger when you enter /blog/post/list/page/.
    # In general, it means: "request page_number, if it does not work, request 1."
    # You can delete "or 1" as a test and enter "/blog/post/list/page/". Interesting things happen :)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1, on_each_side=1, on_ends=2)
    
    # One of the highlights of MTV's Django architecture is context. Contexts are Python dictionaries
    # (usually dictionaries) that move information between the Template and the View as key and value.
    # We can later use the keys sent in the context in the Django Template Engine.
    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "page_number": page_number,
        "paginator": paginator,
        "tags_list": tags_list,
        "categories": categories_list,
        "tag": tag,
        "current_post_author": current_posts_author,
    }

    # And we are nearing the end of our View! Here and in this function we return the render function, which gives us
    # many possibilities. In general, it is a simple bridge between View and Template [Engine]. We pass the request
    # value to the render, then pass the Template address to the render, and finally pass the dictionary/context
    # variable to the render, and a complete MTV is formed. The right relationship between queries, Back-End settings
    # and applications, and finally the display of templates and template features!
    return render(request, "blog/post_list.html", context)


def searched_post_list_view(request):
    form = PostSearchForm()
    query = None
    result = []
    
    if "query" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            # Weights: A -> 1.0, B -> 0.4, C -> 0.2, D -> 0.1
            search_vector = SearchVector("title", weight="A") + SearchVector("description", weight="B") + SearchVector("content", weight="C")
            
            search_query = SearchQuery(query)
            result = Post.actives.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))\
                .filter(search=query).filter(rank__gte=0.2).order_by("-rank")
                
    return render(request, "blog/post_list.html", {"form": form, "query": query, "posts": result})


def post_detail_view(request, slug):
    """
    Little by little, the project is being completed :) Welcome to DetailViews in Django. The previous type we used in
    the previous function was actually a ListView. It would return us a list that we could loop over.
    (with the help of queries:)

    Here the story is a little different. We need a detail instead of a list. In fact, we need to retrieve a specific
    object from the database so that the user can see the details of a post.
    There is very little difference, not really noticeable. You see, to request an Object from the database, we need to
    call it with a specific and unique field. In fact, the database automatically assigns each model an ID field that
    we can use to call Posts, but we already set a Slug field on the Post model, which is ironically exclusive and
    unique.

    Here a possibility comes to us (in Django ORM System) called get. get makes it possible to call an Object from the
    database with a unique field. Now with what? slug. Slugs are good options for this. But, but where does this slug
    fill? Isn't it specific and different for each post?
    """

    # Well, this is where the story gets interesting. We check here whether the object that was called with a special
    # and unique slug exists or not!
    # NOTE THAT: You can do the following process with a function called the get_object_or_404() .
    try:
        # Welcome to nested Queries collection:) Maybe you have a question, why so many queries? The queries here
        # contain a lot of security and filtering load so that if possible, an intruder (hacker) practically cannot
        # inject anything into our queries or get additional information.

        # Of course, this penetration is called "SQL Injection".

        # SQL Injection is protected by default in Django, but in very large projects it is recommended to query your
        # code more precisely, in order to achieve greater vulnerability protection.
        # For example, we have coded the same query twice: .filter(active=True).exclude(active=False) Actually filters
        # return different objects for us based on a specific field, but exclude based on A special field returns
        # various objects and somehow deletes them and does not display them.
        post = Post.objects.all().filter(active=True).exclude(status=str(0)).filter(status=str(1)).\
            filter(category__active=True).filter(pub_datetime__lte=timezone.now()).\
                filter(pub_datetime__lt=timezone.now()).exclude(pub_datetime__gte=timezone.now()).\
                    exclude(pub_datetime__gt=timezone.now()).get(slug=slug)

        # There is a little of complexity here. Explaining this part is not easy, and you should definitely get it
        # with experience.
        # You need to know that in this section we want to get posts similar to this post. A tool is needed for this,
        # what better tool than tagging system?
        # First, we get the tags of this post and then query them.
        post_tags = post.tags.values_list("id", flat=True)

        # This is not much different from previous queries. We will learn a little more about using the django-taggit
        # package. We get to know a new type of query named ("annotate"). Annotate requires additional studies and
        # explanation is not enough for them. Just know that annotate clears equals.
        # On the other hand, we do an additional task: filtering posts whose tags are similar.
        similar_posts = Post.objects.all().filter(active=True).exclude(active=False).filter(category__active=True).\
            exclude(status="0").filter(pub_datetime__lte=timezone.now()).exclude(pub_datetime__gte=timezone.now()).\
                filter(tags__in=post_tags).annotate(same_tags=models.Count("tags")).exclude(pk=post.id).\
                    order_by("-same_tags").order_by("-pub_datetime")[:2]

        # Here is a simple (but interesting) live querying system in Django and MTV. Here, whenever the user opens the page,
        # a view is added to the views' field in the database.
        post.views = post.views + 1
        post.save()

        # Here, like post_list_view, we filter those types of fields that we need so that we are aware, for example,
        # the posts whose activation status is off in the database are not displayed and...
    except ObjectDoesNotExist:
        # If the desired object is not in the database, 404 or (not found!) will be returned.
        raise Http404


    context = {
        "post": post,
        "tags_list": tags_list,
        "categories": categories_list,
        "similar_posts": similar_posts,
    }

    # Here too, the desired object is sent by a dictionary. But where are the slugs filled??? Check the blog/urls.py
    # file.
    return render(request, "blog/post_detail.html", context)


def author_post_list_view(request, author_username):
    """
    excellent. QURNO has been completed to a very large extent. This function is no different from the previous
    functions, it only displays posts related to a specific author.
    """
    try:
        author = CustomUser.objects.filter(is_author=True).exclude(is_author=False).get(username=author_username)
    except ObjectDoesNotExist:
        raise Http404

    try:
        author_posts = author.user_blog_posts.all().filter(active=True).exclude(active=False).\
                filter(category__active=True).exclude(category__active=False).filter(pub_datetime__lte=timezone.now()).\
                    exclude(pub_datetime__gte=timezone.now()).filter(status=str(1)).exclude(status=str(0))
    except ObjectDoesNotExist:
        raise Http404

    paginator = Paginator(author_posts, 25)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1, on_each_side=1, on_ends=2)

    context = {
        "author": author,
        "author_posts": page_obj,
        "page_number": page_number,
        "tags_list": tags_list,
        "categories_list": categories_list,
    }
    return render(request, "blog/author_post_list.html", context)


def category_list_view(request):

    return render(request, "blog/category_list.html", {"categories": categories_list, "tags_list": tags_list})


def category_detail_view(request, slug):
    try:
        category = Category.objects.get(active=True, slug=slug)
        category_posts = category.category_blog_posts.filter(active=True).exclude(status="0").filter(category__active=True)\
                    .filter(pub_datetime__lte=timezone.now()).filter(pub_datetime__lt=timezone.now())
    except ObjectDoesNotExist:
        raise Http404
    
    return render(request, "blog/category_detail.html", {"category": category, 
                                                         "category_posts": category_posts, 
                                                         "tags_list": tags_list,
                                                         "categories": categories_list, })


def tag_list_view(request):
    tags = Tag.objects.all()
    
    return render(request, "blog/tag_list.html", {
        "tags": tags,
        "tags_list": tags_list,
        "categories": categories_list,
    })
