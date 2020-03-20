from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    ListView, 
)

# Create your views here.
from users.models import CustomUser

class ScoreBoardListView(ListView):
    template_name = "scoreboard/scoreboard.html"
    queryset = CustomUser.objects.all()