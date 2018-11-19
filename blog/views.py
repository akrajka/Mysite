from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from blog.models import BlogPost

def blog(request):
    posts = BlogPost.objects.all()
    t = loader.get_template("blog.html")
    c = { 'posts': posts }
    return HttpResponse(t.render(c))

def main(request):
    t = loader.get_template("main.html")  
    return HttpResponse(t.render())