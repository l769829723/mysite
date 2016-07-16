from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.http import JsonResponse
# from .models import Article

# Create your views here.

def home(request):
    return HttpResponse('Hello world!')

def saveArticle(request):
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse({'status': 'ok'}, content_type="application/json")