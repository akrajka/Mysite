from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from pizza.models import Pizza
from django.template.context_processors import media
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, FileResponse


def zlist(request):    
    query=Pizza.objects.all().order_by('id')
    t = loader.get_template("listz.html")    
    c = { 'query': query }
    return HttpResponse(t.render(c))
	