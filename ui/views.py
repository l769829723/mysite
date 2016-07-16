from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('There is UI home.')


class Admin(TemplateView):

    template_name = 'backend/base-admin.html'

class Add(TemplateView):
    template_name = 'backend/add-article.html'