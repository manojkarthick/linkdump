from django.shortcuts import render, redirect
from .models import Link
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

@login_required
def quickadd(request):
    if request.method == 'POST':
        url = request.POST['the_url']
        r = requests.get(url)
        html = BeautifulSoup(r.text,'html.parser')
        if html.title and html.title.text:
            title = html.title.text
        else:
            title = url
        
        link = Link(title=title,url=url,owner=request.user)
        link.save()

        response_data = {}

        response_data['result'] = 'URL Creation successful.'
        response_data['urlpk'] = link.pk
        response_data['url'] = link.url
        response_data['title'] = link.title
        response_data['shortened_url'] = link.shortened_url
        response_data['date_modified'] = link.date_modified.strftime('%B %d, %Y %I:%M %p')

        return HttpResponse(json.dumps(response_data),content_type='application/json')

    else:
        return HttpResponse(json.dumps({"status": "some error encountered"}),content_type='application/json')

@login_required
def index(request):
    links = Link.objects.filter(owner=request.user).order_by('-date_modified')[:3]
    context = {'links': links }
    return render(request,'linksapp/index.html',context)

@login_required
def update_index_table(request):
    links = Link.objects.filter(owner=request.user).order_by('-date_modified')[:3]
    context = {'links': links }
    return render(request,'linksapp/list.html',context)

@login_required
def set_tag_hrchy(request):
    context = {}
    return render(request,'linksapp/tag_hierarchy.html',context)


class AllView(LoginRequiredMixin,generic.ListView):
    template_name = 'linksapp/all.html'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user).order_by('-date_modified')

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Link
    template_name = 'linksapp/detail.html'


class LinkCreate(LoginRequiredMixin,CreateView):
    model = Link
    fields = ['title', 'url', 'description', 'tags', 'shortened_url']
    template_name = 'linksapp/create.html'

class LinkDelete(LoginRequiredMixin,DeleteView):
    model = Link
    template_name = 'linksapp/delete.html'
    success_url = reverse_lazy('linksapp:index')

class LinkUpdate(LoginRequiredMixin,UpdateView):
    model = Link
    template_name = 'linksapp/update.html'
    fields = ['title', 'url', 'description', 'tags', 'shortened_url']
    success_url = reverse_lazy('linksapp:index')

@login_required
def increment_hits(request,link_id):
    link = Link.objects.get(pk=link_id)
    link.hits += 1
    link.save()
    return redirect(link.url)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request,'registration/signup.html',{'form': form})