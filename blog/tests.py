from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Post, Category

# Create your tests here.


class PostTestCase(TestCase):
    """
    Welcome to the tests section. In this section, you will deal with different methods and scenarios to challenge your
    web application. In fact, tests have several methods to perform. There are different tests, for example, security
    test, quality test, speed test, etc.

    The tests that are generally used and recommended by the Django development team (which must be in projects) are
    unit tests. Unit tests are formed from small methods and create large test clusters. Unit test clusters are called
    TestCase.
    Tests are mostly written for large projects, because the Python programming language is suitable for debugging small
    projects, but for a large project it is not at all suitable for debugging, perhaps compared to the competing
    programming language PHP. It is in the context of the web. So we suggest that you definitely have test writing for
    big projects.
    QURNO is not a big project (compared to powerful websites) so it doesn't need big tests. We prefer to have a few
    test clusters per app, no more than that is needed. (at least for QURNO)

    A test cluster is like what you see now!

    NOTE THAT the DarkDragons team will not be responsible for explaining the test writing to a high degree, because the
    logic is from the Python programming language, not the Django framework!

    It is enough to read a little about the tests to fully understand what tests we have added and what they test.
    https://docs.djangoproject.com/en/4.0/topics/testing
    """

    user = None
    category = None
    second_category = None
    post = None
    second_post = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="admin",
            first_name="admin",
            last_name="admin",
            password="admin",
        )
        cls.category = Category.objects.create(
            title="TEST CATEGORY 1",
            description="TEST",
            active=True
        )
        cls.second_category = Category.objects.create(
            title="TEST CATEGORY 2",
            description="TEST CATEGORY 2",
            active=False,
        )
        cls.post = Post.objects.create(
            title="FIRST TEST POST",
            content="THIS IS FIRST TEST!",
            pub_datetime=timezone.now(),
            status=str(1),
            category=cls.category,
            author=cls.user,
            message="TEST",
            active=True,
            read_time=5,
            slug="TEST-1",
        )
        cls.second_post = Post.objects.create(
            title="SECOND TEST POST",
            content="THIS IS SECOND TEST!",
            pub_datetime=timezone.now(),
            status="0",
            category=cls.category,
            author=cls.user,
            message="TEST 2",
            active=True,
            read_time=10,
            slug="TEST-2",
        )
        cls.third_post = Post.objects.create(
            title="THIRD TEST",
            content="THIS IS THIRD TEST!",
            pub_datetime=timezone.now(),
            status="1",
            category=cls.category,
            author=cls.user,
            message="TEST 3",
            active=False,
            read_time=10,
            slug="TEST-3",
        )
        cls.forth_post = Post.objects.create(
            title="FORTH TEST",
            content="THIS IS FORTH TEST!",
            pub_datetime=timezone.now(),
            status="1",
            category=cls.second_category,
            author=cls.user,
            message="TEST 4",
            active=True,
            read_time=10,
            slug="TEST-4",
        )

    def test_post_model_str_response(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_list_lazy_url_by_address(self):
        response = self.client.get("/blog/post/list/")
        self.assertEqual(response.status_code, 302)

    def test_post_list_lazy_url_by_name(self):
        response = self.client.get(reverse("blog:post_list_lazy"))
        self.assertEqual(response.status_code, 302)

    def test_post_list_url_by_address(self):
        response = self.client.get("/blog/post/list/page/")
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_not_have_draft_or_0_status_posts(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertNotContains(response, self.second_post.title and self.second_post.message)
        
    def test_post_list_view_not_have_false_active(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertNotContains(response, self.third_post.title and self.third_post.message)
        
    def test_post_list_view_not_have_post_with_false_category_active(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertNotContains(response, self.forth_post.title and self.forth_post.message)

    def test_post_list_view_have_banner_image(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, self.post.banner)

    def test_post_list_view_have_post_title(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, self.post.title)

    def test_post_list_view_have_post_message(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, self.post.author.username or self.post.author.first_name +
                            self.post.author.last_name)

    def test_post_list_view_have_author_avatar_image(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, self.post.author.avatar)
    
    def test_post_list_view_have_read_time_field(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, self.post.read_time)
        
    def test_post_detail_view_url_by_address(self):
        response = self.client.get("/blog/post/detail/{}/".format(self.post.slug))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_url_by_name(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_404_response_for_0_status_post(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.second_post.slug}))
        self.assertEqual(response.status_code, 404)
        
    def test_post_detail_view_404_response_for_false_active_post(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.third_post.slug]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_have_banner_image(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, self.post.banner)

    def test_post_detail_view_have_title(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, self.post.title)

    def test_post_detail_view_have_content(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, self.post.content)

    def test_post_detail_view_have_author_avatar(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.slug]))
        self.assertContains(response, self.post.author.avatar)

    def test_post_detail_view_have_truth_views(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.slug]))
        self.assertContains(response, self.post.views)
        
    def test_post_detail_view_have_read_time_field(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.slug]))
        self.assertContains(response, self.post.read_time)

    def test_post_detail_view_have_author_field(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, self.post.author)
