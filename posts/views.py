from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
import json
from urllib.request import urlopen
from suds.client import Client
from .models import Posts, Comments
from .forms import PostsForm, CommentsForm


def get_posts_from_API(request):
    web_data = urlopen('http://jsonplaceholder.typicode.com/posts').read().decode('utf-8')
    data = json.loads(web_data)
    context = {'posts': data, 'url_redirect': 'api_post_comments'}
    return render(request, 'allposts.html', context)


def get_posts_from_model(request):
    data = Posts.objects.all()
    context = {'posts': data, 'url_redirect': 'model_post_comments',}
    return render(request, 'allposts.html', context)


def get_comments_from_model(request, post_id):
    post = Posts.objects.get(pk=post_id)
    comments = Comments.objects.filter(postId=post_id)
    form = CommentsForm()
    context = {'comments': comments, 'post': post, 'form': form, 'model_view': True}
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
            return HttpResponseRedirect("/posts/model/"+str(post.id))

    return render(request, 'newpost.html', {
        'form': form,
     })


def comment_form(request, post_id):
    if request.method == 'POST':
        if accept_comment(request.user):
            form = CommentsForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data['body']
                qualified_body = qualify_comment_body(body)
                post = Posts.objects.get(pk=post_id)
                comment = Comments.objects.create(name=request.user, body=qualified_body,
                                                  email=request.user.email, postId=post)
                messages.success(request, "Comment Saved")
        else:
            messages.warning(request, "You are not allowes to comment")

    return HttpResponseRedirect(reverse('model_post_comments', args=[post_id]))

def accept_comment(username):
    if settings.SOAP_WS_WORKING:
        client = Client('http://test.hua.gr:8080/approvecomment/services/ApproveCommentImpl?wsdl')
        return client.service.getOccurences(username) < 3
    else:
        return True

def qualify_comment_body(body_content):
    if settings.SOAP_WS_WORKING:
        client = Client('http://test.hua.gr:8080/approvecomment/services/ApproveCommentImpl?wsdl')
        qualified_content = client.service.filter(body_content)
        return qualified_content
    else:
        return body_content