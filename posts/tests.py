from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from . models import Posts

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
