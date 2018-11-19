from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.conf import settings
from django import forms
from django.db.models import Q
from urllib.parse import urlencode
import datetime
import time
import os
from pastebin.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class ListPaste(LoginRequiredMixin,ListView):
    def __init__(self, qset=Paste.objects.all()):
        ListView.__init__(self)	
        queryset = qset        # Tylko te rekordy
    login_url = '/konto/login/'
    redirect_field_name = 'redirect_to'
    model = Paste   
	# Lista obiektów będzie w object_list (możemy ustawić context_object_name)
    def get_context_data(self, **kwargs):
        context = super(ListPaste, self).get_context_data(**kwargs)        
        context['styt']="LISTA GENERYCZNA"
        return context

class ShowPaste(DetailView):
    # Objekt to renderowania to object lub ustaw context_object_name    
    model = Paste    
    def get_context_data(self, **kwargs):
        context = super(ShowPaste, self).get_context_data(**kwargs)   
        nr=self.object.id 
        u=Paste.objects.all()
        xt=sorted([e.id for e in u])  
        if nr in xt:
            xnr=0   	
            while nr>xt[xnr]:
               xnr=xnr+1		           			
            nrp=xt[xnr-1] if xnr>0 else xt[xnr]
            nrn=xt[xnr+1] if xnr<len(u)-1 else xt[xnr]
        else:
            nrp=xnr
            nrn=xnr   		
        context['nrp']=nrp
        context['nrn']=nrn
        context['nr']=nr
        return context
		
class AddPaste(PermissionRequiredMixin, CreateView):
    model = Paste
    permission_required = 'pastebin.add_paste'
    fields=['content','title','syntax','poster']
    success_url = '/paste/list'	
    def get_context_data(self, **kwargs):
        context = super(AddPaste, self).get_context_data(**kwargs)        
        context['styt']="DODAJ"
        return context	


class EditPaste(UpdateView):
    model = Paste
    fields=['content','title','syntax','poster']
    success_url = '/paste/list'		
    def get_context_data(self, **kwargs):
        context = super(EditPaste, self).get_context_data(**kwargs)        
        context['styt']="ZMIEŃ"
        return context	

class DeletePaste(DeleteView):
    model = Paste
    fields=['content','title','syntax','poster']
    success_url="/paste/list"
	#def get_success_url(self):
    #    return reverse('list')
    def get_context_data(self, **kwargs):
        context = super(DeletePaste, self).get_context_data(**kwargs)        
        context['styt']="USUŃ"
        return context	


def write_pdf_view(request, nr=1):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    e = Paste.objects.filter(id=nr).get()
    nl=10*len(e.content.split("\n"))+350

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(595,nl))   

    # Start writing the PDF here
   
    ifile=["plain.jpg","Python.jpg","HTML.jpg","SQL.png","Javascript.jpg","CSS.png"][e.syntax]  
    ifile=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"pastebin","templates",ifile)  
    im = Image.open(ifile)
    p.drawInlineImage(im, 256, nl-150, width=100, height=60)  
    # p.setFont("Helvetica", 14)     
    p.setFont('DarkGardenMK',24)
    p.drawString(100,nl-200,e.title)
    p.line(100,nl-220,500,nl-220)
    p.setFont("Courier", 10)   
    p.setFillColor(colors.red)
    p.setStrokeColor(colors.gray)
 
    sp=nl-250
    for f in e.content.split("\n"):
        f=f[:-1]
        p.drawString(100,sp, f)
        sp=sp-10
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def plista(request):    
    if request.method=="POST":
        query=Paste.objects.all().order_by('id')  
    else:
        wek=request.GET['param']
        if len(wek)>0:
            wek=wek.split(',')
            wek=[int(e) for e in wek] 
            query=Paste.objects.filter(id__in=wek).order_by('id') 
        else:
            query=Paste.objects.all().order_by('id') 
    t = loader.get_template("list.html")    
    c = { 'query': query, 'styt':"LISTA"}
    return HttpResponse(t.render(c))
	
def psearch(request):
    dist1={"Plain":0, "Python":1, "HTML":2, "SQL":3, "Javascript":4,"CSS":5}    
    xdist={}        
    if request.method=='POST':
        for e in ['slowo1', 'slowo2','slowo3','wybor1','wybor2'] :        
            xdist[e]= request.POST.getlist(e)
            if len(xdist[e])>0:
                xdist[e]=xdist[e][0]       
        if len(xdist['slowo1'])>0:
            p=Q(syntax=dist1[xdist['slowo1']])
        else:
            p=Q()
        if len(xdist['slowo2'])>0:
            q=Q(title__icontains=xdist['slowo2'])
            if len(xdist['wybor1'])=='I NIE':
                p=p & ~q
            elif len(xdist['wybor1'])=='LUB NIE':
                p = p | ~q           
            elif len(xdist['wybor1'])=='LUB':
                p = p | q
            else:
                p = p & q
        if len(xdist['slowo3'])>0:
            q=Q(content__icontains=xdist['slowo3'])
            if len(xdist['wybor2'])=='I NIE':
                p = p & ~q
            elif len(xdist['wybor2'])=='LUB NIE':
                p = p | ~q           
            elif len(xdist['wybor2'])=='LUB':
                p = p | q
            else:
                p = p & q              
        queryset=Paste.objects.filter(p)  
        w='/paste/lista?param='                
        for e in queryset:
            w=w+str(e.id).strip()+","
        w=w[:-1:]
        return redirect(w)
    return render(request,"search.html",{})


	


        
