from django.shortcuts import render
import json
from urllib.request import urlopen

# Create your views here.
def index(request):
     data = json.load(urlopen('http://jsonplaceholder.typicode.com/posts'))
     context = {'posts' : data}
     return render(request, 'allposts.html', context)