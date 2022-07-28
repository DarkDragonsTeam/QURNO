from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from extensions.utils import get_jalali_date
from .managers import ActivePostManager

# Create your models here.


class Category(models.Model):
    """
    This class is for Blog related categories. In fact, categories make it easier for viewers to find the basins they
    need. Do not confuse the tagging system with the categorization system! They have a lot of impact on both SEO and
    CMS, but the categorization system is just for the convenience of the user and a little of SEO help.

    The categorization system itself is not necessary, you can delete this (and its dependencies).
    """
    
    title = models.CharField(_("عنوان"), max_length=225, unique=True)
    description = models.TextField(_("توضیحات"), null=True, blank=True)
    designer = models.ForeignKey(verbose_name=_("طراح دسته بندی"), to=get_user_model(), on_delete=models.CASCADE,
                                 related_name="user_blog_categories")
    slug = models.SlugField(_("اسلاگ URL"), max_length=225, unique=True, allow_unicode=True)
    datetime_created = models.DateTimeField(_("تاریخ و زمان ساخت"), auto_now_add=True, auto_now=False)
    datetime_modified = models.DateTimeField(_("تاریخ و زمان آخرین تغییر"), auto_now_add=False, auto_now=True)
    active = models.BooleanField(_("وضعیت فعال سازی"), default=True)

    class Meta:
        # Here we enter the Persian format settings of the model (with Django translator method)
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")
        
        ordering = ("-datetime_modified", )

    # In the following two functions, we specify the names (identifiers) related to our model (class).
    def __unicode__(self):
        if len(str(self.title)) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25])
        
    def __repr__(self):
        if len(str(self.title)) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25])

    def __str__(self):
        if len(str(self.title)) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25])


class Post(models.Model):
    """
    The main part of our project is this model (class). This class is where everything is defined. The posts that are
    made in the project and the pages of our site are in fact examples of this class. We have to engineer and design
    this class very carefully, so that we do not have trouble seeing the results later. As mentioned, this class will
    later become the actual instances and tables in our database, so we need to follow the normalization of the table
    as well (its rules). Study this class and its behaviors carefully.

    Let's first draw in our minds what we want to build!
    We are going to make examples of this class, which are going to become our website posts. Does a post need anything?
    A post, as a title, a content (or body), a creation date time, last modifying date time, an author, a publishing
    date time, and a Slug URL (we'll talk about them later in the views) and a publishing status requirement has it.
    At least that's what he needs at least! In fact, it may be more advanced.

    We have to make sure that the fields we create have the right types and choices, because they have a direct impact
    on the processing speed of our site. Try not to manipulate the type of fields, they are designed in the most
    standard way possible.
    """

    STATUS_CHOICES = (
        ("0", _("پیش نویس"), ),
        ("1", _("منتشر شده"), ),
    )

    banner = models.ImageField(_("بنر"), upload_to="blog/post/", blank=True,
                               default="defaults/blog_post_default_banner.png")
    title = models.CharField(_("عنوان"), max_length=225)

    # To use this field, you must be familiar with the Django CKEditor package. This package allows you to have a
    # powerful text editor. In fact, the type that is stored is the same as TextField(), with a slight change, we
    # introduce, RichTextFields! RichTextFields saves HTML and CSS commands quickly and automatically
    # (with pointers like Office) and gives your instance a beautiful format.
    content = RichTextUploadingField(_("محتوا"))

    description = models.CharField(_("توضیحات"), max_length=225, unique=True)
    author = models.ForeignKey(verbose_name=_("نویسنده"),
                               to=get_user_model(), on_delete=models.CASCADE, related_name="user_blog_posts")
    datetime_created = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("آخرین تغیر"), auto_now=True)
    slug = models.SlugField(_("اسلاگ URL"), max_length=225, unique=True, allow_unicode=True)
    pub_datetime = models.DateTimeField(_("تاریخ انتشار"), default=timezone.now, blank=True)
    category = models.ForeignKey(verbose_name=_("دسته بندی"), to=Category, on_delete=models.CASCADE,
                                 related_name="category_blog_posts")
    tags = TaggableManager(_("تگ ها"), blank=True)
    read_time = models.PositiveSmallIntegerField(_("مدت زمان مورد نیاز برای مطالعه"), default=5)
    status = models.CharField(_("وضعیت"), max_length=225, choices=STATUS_CHOICES, default="0")
    active = models.BooleanField(_("وضعیت فعال سازی"), default=True)
    views = models.PositiveBigIntegerField(_("بازدید ها"), default=0, blank=True)
    # Managers
    objects = models.Manager()
    actives = ActivePostManager()

    def get_pub_datetime_jalali_date(self):
        """
        As you know, date[time] is never saved in Solar/Jalali in the database. This method has the task of receiving
        the Gregorian date and converting it to Solar/Jalali. If you have read the files carefully, there is a file
        in "extensions" directory called "utils.py" in which the contents of this method are written
        (and we have explained about it in full)
        """
        return get_jalali_date(self.pub_datetime)
    # This command is related to the above method (get_pub_datetime_jalali). Here we specify what the external name of
    # the method (what is displayed) is.
    get_pub_datetime_jalali_date.short_description = _("تاریخ انتشار")

    # This function (as shown above) is responsible for creating a small banner to display in the admin panel.
    # Note that this whole function returns a normal string, but for security reasons Django does not display it.
    # In fact, our HTML and CSS commands will not be applied. For this reason, we use the format_html function,
    # which is built internally in Django. This function makes our commands appear in real and raw HTML and CSS.
    def get_banner_thumbnail(self):
        return format_html("""
        <span>
            <img src="{}" style="height: 95.5px; width: 135.5px;" />
        </span>
        """.format(self.banner.url))
    get_banner_thumbnail.short_description = _("بنرِ پست")

    class Meta:
        """
        Here are your model settings. You customize your model here and assign more settings (Meta) to this model than
        you previously designed. In fact, it will give you a wide range of possibilities, if you can work with it.
        It is more related to the database, but it is also a general setting for Django.
        """

        # Persian format settings
        verbose_name = _("پست")
        verbose_name_plural = _("پست ها")

        # Well, excellent. So far our model is ready to launch. But one more thing remains, the order, and the basis
        # of the order of this model. The order base causes posts to be sorted based on a specific field in the
        # database, for example with the pub_datetime field, when we connect this field to the database for order, the
        # database places the posts by date at the bottom, For example, the post that was published on September 1 is
        # placed first, and the next post that was published on September 2 is placed in front of it.

        # So what do we do to get the latest posts at the top? To do this, we need to enter one - behind the field we
        # want in the lower variable/Tuple.
        ordering = ("-datetime_modified", )

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __unicode__(self):
        if len(str(self.title)) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25] + "...")

    def __repr__(self):
        if len(self.title) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25] + "...")

    def __str__(self):
        if len(str(self.title)) <= 25:
            return str(self.title)
        else:
            return str(self.title[:25] + "...")


class Comment(models.Model):
    post = models.ForeignKey(verbose_name=_("پست"), to=Post, on_delete=models.CASCADE, 
                             related_name="blog_post_comments")
    author = models.ForeignKey(verbose_name=_("کامنت های کاربر"), to=get_user_model(), 
                               on_delete=models.CASCADE, related_name="user_blog_post_comments")
    datetime_created = models.DateTimeField(_("تاریخ و زمان ساخت"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_(("تاریخ و زمان آخرین دستکاری")), auto_now=True)
    title = models.CharField(_("عنوان"), max_length=225, null=True, blank=True)
    text = models.TextField(_("متن نظر"))
    active = models.BooleanField(_("وضعیت فعال سازی"), default=False)
    read = models.BooleanField(_("خوانده شده"), default=False)
    
    def get_text_thumbnail(self):
        if len(str(self.text)) <= 25:
            return format_html("""
                               <p>{}</p>
                               """.format(str(self.text[:25])))
        else:
            return format_html(str("""
                                   <p>{}</p>
                                   """.format(str(self.text[:25])) + 
                                   "..."))
    get_text_thumbnail.short_description = _("متن")
    
    def get_datetime_created_jalali_date(self):
        return get_jalali_date(self.datetime_created)
    
    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")
        
        ordering = ("-datetime_created", )

    def __unicode__(self):
        return str(self.author)

    def __str__(self):
        return str(self.author)

    def __repr__(self):
        return str(self.author)
