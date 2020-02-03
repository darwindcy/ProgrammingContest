from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    DetailView, 
    ListView, 
    UpdateView, 
    DeleteView
)

from .models import Contest

class ContestListView(ListView):
    template_name = "contests/contest_list.html"
    queryset = Contest.objects.all()