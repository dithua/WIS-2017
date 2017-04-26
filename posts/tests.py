from django.test import TestCase, Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from . models import Posts
from . forms import PostsForm
# -------- Model tests --------------

class PostsModelTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='testuser')
        self.post = Posts(userId = self.test_user, title="My post title", body="My post body")

    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.post._meta.verbose_name_plural), "posts")

    def test_save_post_without_user(self):
        post = Posts(title="My post title", body="My post body")
        self.assertRaises(IntegrityError, post.save )

    def test_save_post_with_user(self):
        self.assertTrue(self.post.save )


# ---------  Form Tests ----------------

class PostsFormTest(TestCase):

    def test_form_without_data(self):
        form = PostsForm({
            'title': "",
            'body': "",
        })
        self.assertFalse(form.is_valid())

    def test_form_without_title(self):
        form = PostsForm({
            'title': "",
            'body': "My post body",
        })
        self.assertFalse(form.is_valid())

    def test_form_without_body(self):
        form = PostsForm({
            'title': "My post title",
            'body': "",
        })
        self.assertFalse(form.is_valid())

    def test_form_with_data_and_body(self):
        form = PostsForm({
            'title': "My post title",
            'body': "My post body",
        })
        self.assertTrue(form.is_valid())


# -------------- View Tests ----------------

class PostsViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/posts/model/')
        self.assertEqual(resp.status_code, 200)