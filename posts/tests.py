from django.test import TestCase, Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api_posts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_index_uses_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('post_new'))
        self.assertRedirects(resp, '/accounts/login/?next=/posts/new/')

    def test_logged_in_uses_correct_template(self):
        test_user = User.objects.create_user(username='testuser', password='1234qwer')
        login = self.client.login(username='testuser', password='1234qwer')
        resp = self.client.get(reverse('post_new'))
        self.assertEqual(str(resp.context['user']), 'testuser')
        self.assertEqual(resp.status_code, 200)

    def test_new_model_button_exist(self):
            response = self.client.get('/posts/model/')
            self.assertContains(response, 'New Post')

