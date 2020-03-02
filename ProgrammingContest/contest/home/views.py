from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class Homepageview(TemplateView):
    template_name = "home/homepage.html"