from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import (
    ScoreBoardListView
)

app_name = 'scoreboard'

urlpatterns = [
    path('', ScoreBoardListView.as_view(), name='scoreboard'),
]