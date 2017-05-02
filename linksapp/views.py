from django.shortcuts import render, redirect
from .models import Link,Tag
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


def index(request):
    links = Link.objects.order_by('-date_modified')[:3]
    context = {'links': links }
    return render(request,'linksapp/index.html',context)

class AllView(generic.ListView):
    template_name = 'linksapp/all.html'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.objects.all().order_by('-date_modified')

class DetailView(generic.DetailView):
    model = Link
    template_name = 'linksapp/detail.html'

class LinkCreate(CreateView):
    model = Link
    fields = ['title','url','description','tags','shortened_url']
    template_name = 'linksapp/create.html'

class LinkDelete(DeleteView):
    model = Link
    template_name = 'linksapp/delete.html'
    success_url = reverse_lazy('linksapp:index')

class LinkUpdate(UpdateView):
    model = Link
    template_name = 'linksapp/update.html'
    fields = ['title','url','description','tags','shortened_url']
    success_url = reverse_lazy('linksapp:index')

def increment_hits(request,link_id):
    link = Link.objects.get(pk=link_id)
    link.hits += 1
    link.save()
    return redirect(link.url)

