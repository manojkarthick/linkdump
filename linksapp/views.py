from django.shortcuts import render
from django.http import HttpResponse
from .models import Link,Tag

def index(request):
    links = Link.objects.all()
    context = {'links': links }
    return render(request,'linksapp/index.html',context)
