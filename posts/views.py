from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json
from urllib.request import urlopen
from .models import Posts
from .forms import PostsForm

# Create your views here.
def index(request):
     data = json.load(urlopen('http://jsonplaceholder.typicode.com/posts'))
     context = {'posts' : data}
     return render(request, 'allposts.html', context)

@login_required
def getposts_from_model(request):
     data = Posts.objects.all()
     context = {'data' : data}
     return render(request, 'allposts.html', context)



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
