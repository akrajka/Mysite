from django.contrib import admin
from django.urls import path
from pastebin import models, views
from pastebin.views import ListPaste, ShowPaste, AddPaste, EditPaste, DeletePaste
from pastebin.models import Paste


urlpatterns = [
    path('lista/', views.plista),
    path('search', views.psearch), 
    path('list/', ListPaste.as_view(), name=""),
    path('edit/<int:pk>', ShowPaste.as_view()),    # Uwaga - nazwa pk ważna
    path('edit/pdf/<int:nr>', views.write_pdf_view),
    path('add', AddPaste.as_view()),
    path('change/<int:pk>', EditPaste.as_view()),    # Uwaga - nazwa pk ważna  
    path('del/<int:pk>', DeletePaste.as_view()),    # Uwaga - nazwa pk ważna  
]
