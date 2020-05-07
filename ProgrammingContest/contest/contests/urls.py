from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import (
    ContestListView,
    ContestDetailView,
    ContestDeleteView,
    ContestCreateView,
    ContestUpdateView,
    ContestStartView,
    ContestStopView,
    ProblemDetailView,
    ContestSubmissionsListView,
    ContestScoreBoardView,
    ContestProblemCreateView,
    ContestSubmissionsForTeamView,
    ContestPauseView,
    ContestSubmissionDeleteView
)

from submission.views import SubmissionCreateView

app_name = 'contests'

#URLS in the contest/ link
urlpatterns = [
    path('', ContestListView.as_view(), name = 'contest-list'),
    path('<int:id>/', ContestDetailView.as_view(), name = 'contest-detail'),
    path('<int:id>/delete/', ContestDeleteView.as_view(), name = 'contest-delete'),
    path('create/', ContestCreateView.as_view(), name = 'contest-create'),
    path('<int:id>/update/', ContestUpdateView.as_view(), name = 'contest-update'),
    path('<int:id>/start/', ContestStartView.as_view(), name = 'contest-start'),
    path('<int:id>/stop/', ContestStopView.as_view(), name = 'contest-stop'),
    path('<int:id>/pause/', ContestPauseView.as_view(), name = 'contest-pause'),
    path('<int:id>/problem/<int:problem_id>/', ProblemDetailView.as_view(), name = 'problem-detail'),
    path('<int:id>/submissions/', ContestSubmissionsListView.as_view(), name = 'contest-submissions'),
    path('<int:id>/submissions/delete/', ContestSubmissionDeleteView, name = 'contest-submissions-delete'),
    path('<int:id>/problem/<int:problem_id>/submit/', SubmissionCreateView.as_view(), name = 'contest-submission-create'),
    path('<int:id>/scoreboard/', ContestScoreBoardView.as_view(), name = 'contest-scoreboard'),
    path('<int:id>/problems/create/', ContestProblemCreateView.as_view(), name = 'contest-problem-create'),
    path('<int:id>/submissions/<int:team_id>/', ContestSubmissionsForTeamView.as_view(), name = 'contest-team-submissions')
]