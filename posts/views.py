from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json
from urllib.request import urlopen
from .models import Posts, Comments
from .forms import PostsForm


def get_posts_from_API(request):
    web_data = urlopen('http://jsonplaceholder.typicode.com/posts').read().decode('utf-8')
    data = json.loads(web_data)
    context = {'posts': data, 'url_redirect': 'api_post_comments'}
    return render(request, 'allposts.html', context)


def get_posts_from_model(request):
    data = Posts.objects.all()
    context = {'posts': data, 'url_redirect': 'model_post_comments'}
    return render(request, 'allposts.html', context)


def get_comments_from_model(request, post_id):
    post = Posts.objects.get(pk=post_id)
    comments = Comments.objects.filter(postId=post_id)
    context = {'comments': comments, 'post': post}
    return render(request, 'post_comments.html', context)


def get_comments_from_API(request, post_id):
    web_comments = urlopen('http://jsonplaceholder.typicode.com/posts/'+str(post_id)+"/comments").read().decode('utf-8')
    comments = json.loads(web_comments)
    web_post = urlopen('http://jsonplaceholder.typicode.com/posts/'+str(post_id)).read().decode('utf-8')
    post = json.loads(web_post)
    context = {'comments': comments, 'post': post}
    return render(request, 'post_comments.html', context)

def post_form(request):
    if request.method == 'GET':
        form = PostsForm()
    else:
        form = PostsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            post = Posts.objects.create(title=title,body=body,userId = request.user)
            return HttpResponseRedirect("/posts/"+str(post.id))

    return render(request, 'newpost.html', {
        'form': form,
     })
