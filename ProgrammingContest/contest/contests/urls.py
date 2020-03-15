from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import (
    ContestListView,
    ContestDetailView,
    ContestDeleteView,
    ContestCreateView,
    ContestUpdateView,
    ContestDetailTeamView,
    ProblemCreateView,
    ContestStartView,
    ContestStopView
)

app_name = 'contests'

urlpatterns = [
    path('', login_required(ContestListView.as_view()), name = 'contest-list'),
    path('<int:id>/', login_required(ContestDetailView.as_view()), name = 'contest-detail'),
    path('<int:id>/delete/', login_required(ContestDeleteView.as_view()), name = 'contest-delete'),
    path('create/', login_required(ContestCreateView.as_view()), name = 'contest-create'),
    path('<int:id>/update/', login_required(ContestUpdateView.as_view()), name = 'contest-update'),
    path('problems/create/', ProblemCreateView.as_view(), name = 'problem-create'),
    path('<int:id>/start/', ContestStartView.as_view(), name = 'contest-start'),
    path('<int:id>/stop/', ContestStopView.as_view(), name = 'contest-stop')
]