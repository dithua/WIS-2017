from django.conf.urls import include, url
from posts import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
]