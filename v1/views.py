from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from agent.task import _my_background_task

# Create your views here.

def home(request):
    return HttpResponse('Hello world.')

class Hello(View):
    def get(self):
        _my_background_task.delay('Green pine')
        return HttpResponse('Hello world!!!')