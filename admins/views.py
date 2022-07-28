"""
Welcome to the administration section. This part has been one of the honors and the longest parts of QURNO during
development. In fact, this part is the result of experience. You have to work and gain effective experiences to
understand this part.

We will give general explanations in this regard, but of course you will not know until you implement it practically
and with practice.

In this part, we want to create a personal management, you must know what this type of software design is like. In fact,
the logic of management panels is much more tangible in other languages; For example in PHP language.
Administrations allow you to go back and forth between different parts of the site. They allow you to see and review
your personal projects; Pay attention to what you have done and finally become a complete administrator for the site.
Of course, management can be given to other users, in this project, we have used the is_author status, which checks
whether the user is an author (the same manager) or not.

Again, we repeat that your understanding of this part depends on your experience with Django and even sometimes with Web
and JavaScript, because not all pieces of code are made with the Django framework and the Python programming language.
"""


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .forms import UserForm

from blog.models import Post, Category, Comment
from blog.forms import PostForm, CategoryForm, MiniPostCreateForm, PostSearchForm
from accounts.models import CustomUser
from extensions.utils import get_jalali_today

# Create your views here.

global today
today = get_jalali_today()


@login_required()
def admin_portal_view(request):
    """
    This is the admin portal, the scene the admin will see on first encounter. The portal should be designed in a neat,
    beautiful and short way, so that it is also efficient and able to provide the best service to the manager.

    Here we show the administrator a short list of personal posts and allow him to quickly edit, delete or publish his
    personal posts.

    We enter very heavy and large queries here, of course, the speed efficiency will decrease, on the other hand, QURNO
    templates do not have global standards and are created only for development, so be careful to use templates with
    global standards for the management portal. And use light, because very heavy queries are entered in it.
    """
    if not request.user.is_author and not request.user.is_staff:
        # Here we check whether the user has the is_author status turned on or not. Of course, if the user has the
        # status of is_staff turned on, we can accept to enter the management, we will have this part in all View
        # functions, so remember it.
        return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    # Here it is also known what queries have been made (variable names can have direct references to the function of
    # the variable.)
    total_posts = Post.objects.count()
    total_actives_posts = Post.actives.count()
    total_comments = Comment.objects.count()
    total_users = get_user_model().objects.count()
    recent_posts = Post.objects.filter(author=request.user).order_by("-datetime_created")[:10]

    # This is also a simple pagination system, and no additional explanation is needed, this pagination is already built
    # and explained in the Django documentation.
    paginator = Paginator(recent_posts, 3)
    page_num = request.GET.get("page")
    try:
        recent_posts = paginator.get_page(page_num)
    except PageNotAnInteger:
        recent_posts = paginator.get_page(1)
    except EmptyPage:
        recent_posts = paginator.get_page(paginator.num_pages)

    # In this section, we use Django's internal forms and create a quick post creation form, which can help the
    # administrator a lot.
    post_create_form = MiniPostCreateForm()
    if request.POST:
        # We emphasize: these types of forms are wrong. You have to create different functions and handle your form
        # through that. (FORM ACTIONS), but this method is much faster and more accessible (ATTENTION: in the
        # development stages of QURNO, it was decided to use this type of design of forms, because they are easier and
        # more understandable and faster to design, the concept of this The forms are self-explanatory and there is no
        # need to explain them.)
        query = request.POST["query"]
        requested = request.POST["requested"]
        value = request.POST["value"]
        if query == "post":
            post = Post.objects.get(id=int(value))
            if requested == "publish_post":
                post.active = True
                post.status = "1"
                post.pub_datetime = timezone.now()
                post.save()
                return redirect("blog:post_detail", post.slug)
            elif requested == "deactivation":
                post.active = False
                post.save()
                return HttpResponseRedirect(request.path_info)
        elif requested == "post_create":
            post_create_form = MiniPostCreateForm(request.POST)
            if post_create_form.is_valid():
                commit = post_create_form.save(commit=False)
                commit.author = request.user
                commit.save()
                # ->
                post_create_form.save_m2m()
                return redirect("admins:post_detail", Post.objects.first().id)

    context = {
        "total_posts": total_posts,
        "total_actives_posts": total_actives_posts,
        "total_comments": total_comments,
        "total_users": total_users,
        "recent_posts": recent_posts,
        "post_create_form": post_create_form,
        "today": today,
    }
    return render(request, "admins/portals/admin_portal.html", context)


@login_required()
def admin_profile_view(request):
    """
    It is a joint Detail View and UpdateView. In fact, on this page, we provide both a Detail View and a Update View to
    the intended user. The user can edit or manipulate his personal information on the site :)
    """
    if not request.user.is_author and not request.user.is_staff:
        return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    # First, we need to have access to the intended user. The best solution for this idea is to obtain user information
    # through the "request" variable.
    user = request.user

    # Now we refer to the "user" variable that we created earlier and try to fill the user information from the "user"
    # instance. But the user may have entered certain information, so first we fill in the values and if Python (by or)
    # realizes that there is no value in the form, it will return None. "user" and fill the form based on the user's
    # previous information.
    form = UserForm(data=request.POST or None, files=request.FILES or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)

    return render(request, "admins/portals/user_profile.html", {"form": form})


@login_required()
def admin_terms_view(request):
    """
    This view is only for displaying a template in which the rules of the website are displayed.
    """
    if not request.user.is_author and not request.user.is_staff:
        return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    return render(request, "admins/portals/admin_terms.html", {"today": today})


@login_required()
def post_list_view_lazy(request):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    return HttpResponseRedirect("/admins/blog/post/list/page/")


@login_required()
def post_list_view(request, author_username=None):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    # Here we also check that if the user entered the author_username value through the URLs, it will return the posts
    # related to that user.
    if author_username:
        try:
            author = get_user_model().objects.get(username=author_username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(request, "admins/errors/404.html")

        posts = Post.objects.all().filter(author=author)
        paginator = Paginator(posts, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1, on_each_side=1, on_ends=2)
    else:
        author = None

        posts = Post.objects.all()
        paginator = Paginator(posts, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1, on_each_side=1, on_ends=2)

    context = {
        "page_obj": page_obj,
        "posts": page_obj,
        "page_number": page_number,
        "author_username": author_username,
        "author": author,
        "today": today
    }
    return render(request, "admins/blog/post_list.html", context)


@login_required()
def searched_post_list_view(request):
    """
    ATTENTION: To use this section, you must use a PostgreSQL database. The PostgreSQL database provides us with an
    internal search engine for the website, which we prefer to use, because it is very accurate and fast, and has
    powerful queries.

    To use this section, you must have the knowledge of using PostgreSQL and Django PostgreSQL Contrib, which you can
    obtain in your Django documentation.
    """
    if not request.user.is_author and not request.user.is_staff:
        return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    
    form = PostSearchForm()
    query = None
    result = []
    
    if "query" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            search_vector = SearchVector("title")
            search_query = SearchQuery(query)
            result = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))\
                .filter(search=query).order_by("-rank")
                
    return render(request, "admins/blog/post_list.html", {"form": form, "query": query, "posts": result,
                                                          "today": today})


@login_required()
def post_detail_view(request, pk):
    """
    These examples of DetailViews are not dependent on SlugFields and instead work with the Primary Key of the table in
    question.
    """
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    return render(request, "admins/blog/post_detail.html", {"post": post, "time_now": timezone.now()})


@login_required()
def post_create_view(request):
    """
    Here we want to add posts in our admin panel, so the task of this function is to create posts.

    Welcome to the Create View sections. Create Views are constructs for executing and adding, and (creating) an object
    in the database. We have already seen the example of CreateViews in Django Admin Panel, but it is not enough and, we
    will implement a simpler version (or with different views more professional :)) of it.

    To use Create Views we must have a form, which is designed and implemented from a specific model. This form is a
    copy of the same database objects, except that it is empty and (ready to) be filled.
    """
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    form = None

    # Here we also check that if the user sent a POST request, check the form and save it if it is valid, otherwise
    # return the blank form.
    if request.method == "POST":
        # In this section, we have entered the condition, that is, Python has realized that a POST request has been sent
        # to us and must check it, definitely when a POST request is sent, it will bring information with it, we have
        # this We pass the information to the PostForm and send it. (ATTENTION: The request.FILES value is sent only
        # when your form contains file information such as photos, music, video, etc.)
        form = PostForm(request.POST, request.FILES)

        # In this section, we check whether the information is correct or not, for example, spy scripts should not enter
        # the site through these forms, or for example, we should not allow unauthorized files or incomplete information
        # to be sent through these entries.
        # ATTENTION: An example of sending malicious files is sending PHP and JavaScript (sometimes Perl) scripts. When
        # these files are entered into the program, the server automatically opens them because the servers are
        # basically ready to process these languages (especially PHP).
        if form.is_valid():
            # When we enter this condition, we are sure that the forms are secure and have no information defects
            # (or leaks); So we can store them safely and be sure that no problem will occur. But the point is that
            # commits allow the developer to have an opportunity to save information; When a
            # commit = form.save(commit=True) occurs, it means (Keep the form information for now, I have other things
            # to do.)

            # We do not ask the author of the post here (when receiving the form), but here we save it automatically in
            # a commit.
            commit = form.save(commit=False)
            commit.author = request.user
            commit.save()
            # Here we also use save_m2m() to save tags.
            form.save_m2m()
            return redirect("admins:post_detail", Post.objects.first().id)
        else:
            form = PostForm()
    elif request.method == "GET":
        form = PostForm()


    context = {
        "form": form,
        "today": today,
    }
    return render(request, "admins/blog/post_create.html", context)


@login_required()
def post_update_view(request, pk):
    """
    This is a raw Update View. The previous example was semantically considered a Detail View in addition to an
    Update View.

    Here we need to get the information of a specific post and perform various operations on it. The user may need to
    change a certain field, and the rest of the fields don't need to be changed, so we need to get an example from the
    user's previous post so that if he enters a blank value (he didn't actually change it) Do not manipulate and save
    previous information.
    """
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    post = None
    form = None

    try:
        post = Post.objects.get(id=pk)

        if post.author != request.user:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        commit = form.save(commit=False)
        commit.author = request.user
        commit.save()
        form.save_m2m()
        return redirect("admins:post_detail", Post.objects.first().id)

    return render(request, "admins/blog/post_update.html", {"form": form, "post": post, "today": today})


@login_required()
def post_delete_view(request, pk):
    """
    This is a Delete View. Delete views are used to delete a specific value from the database. In fact, their work is
    generally similar to Detail Views, but with the difference that after receiving the desired value, they check it
    and, if necessary, call the delete() method, and thus the post is deleted, and then We will be directed to the list
    of posts.
    """
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    post = None
    form = None

    try:
        post = Post.objects.get(id=pk)

        if request.user != post.author:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    if request.method == "POST":
        post.delete()
        return redirect("admins:post_list")

    return render(request, "admins/blog/post_delete.html", {"form": form, "post": post, "today": today})


@login_required()
def category_list_view_lazy(request):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    return HttpResponseRedirect("/admins/post/category/page/")


@login_required()
def category_list_view(request, category_designer_username=None):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    category_designer = None
    if category_designer_username:
        try:
            category_designer = CustomUser.objects.get(username=category_designer_username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(render(request, "admins/errors/404.html"))

        categories = Category.objects.filter(designer=category_designer)
    else:
        categories = Category.objects.all()

    paginator = Paginator(categories, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1, on_each_side=1, on_ends=2)

    return render(request, "admins/blog/category_list.html", {"categories": page_obj, "page_obj": page_obj,
                                                              "category_designer": category_designer, "today": today})


@login_required()
def category_detail_view(request, pk):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    try:
        category = Category.objects.get(id=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    category_posts = category.category_blog_posts.all()

    return render(request, "admins/blog/category_detail.html", {"category": category,
                                                                "category_posts": category_posts,
                                                                "today": today, })


@login_required()
def category_create_view(request):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    form = None

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.designer = request.user
            commit.save()
            return redirect("admins:category_detail", Category.objects.first().id)
    elif request.method == "GET":
        form = CategoryForm()

    return render(request, "admins/blog/category_create.html", {"form": form, "today": today})


@login_required
def category_update_view(request, pk):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    category = None
    form = None

    try:
        category = Category.objects.get(id=pk)
        if category.designer != request.user:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("admins:category_detail", category.id)

    return render(request, "admins/blog/category_update.html", {"category": category, "form": form, "today": today})


@login_required()
def category_delete_view(request, pk):
    if not request.user.is_author and not request.user.is_staff:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))

    try:
        category = Category.objects.get(id=pk)

        if category.designer != request.user:
            return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "admins/errors/404.html"))

    if request.method == "POST":
        category.delete()
        return redirect("admins:category_list")

    return render(request, "admins/blog/category_delete.html", {"category": category, "today": today})


@login_required()
def admin_profile_view(request):
    if not request.user.is_author and not request.user.is_admin:
        return HttpResponseForbidden(render(request, "admins/errors/403.html"))
    
    user = get_user_model().objects.get(username=request.user.username)
    
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(data=request.POST or None, files=request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = UserForm()
        
    return render(request, "admins/portals/admin_profile.html", {"form": form, "user": user, "today": today})
