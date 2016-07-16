from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Celery task
from .task import add as task_add

# Create your views here.

def home(request):
    return HttpResponse('Hello world!')

def add(request):
    a = request.GET.get('a', '0')
    b = request.GET.get('b', '0')
    result = task_add(int(a), int(b))
    return HttpResponse('The result is: %s .' % str(result))