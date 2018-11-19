from django.contrib import admin
from django.urls import path, re_path, include
from pizza.models import *
from pizza.views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('menu/', zlist, name='Pizza menu'),
]


