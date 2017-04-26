from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
        url(r'^new/', login_required(views.post_form), name='post_new'),
        url(r'^comment/(?P<post_id>\d+)/$', views.comment_form, name='post_comment'),
        url(r'^model/$', views.get_posts_from_model, name='model_posts'),
        url(r'^model/(?P<post_id>\d+)/$', views.get_comments_from_model, name='model_post_comments'),
        url(r'^api/$', views.get_posts_from_API, name='api_posts'),
        url(r'^api/(?P<post_id>\d+)/$', views.get_comments_from_API, name='api_post_comments'),
]