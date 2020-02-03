from django.urls import path

from .views import (
    ContestListView,
    ContestDetailView,
    ContestDeleteView,
    ContestCreateView,
    ContestUpdateView,
)

app_name = 'contests'

urlpatterns = [
    path('', ContestListView.as_view(), name = 'contest-list'),
    path('<int:id>/', ContestDetailView.as_view(), name = 'contest-detail'),
    path('<int:id>/delete/', ContestDeleteView.as_view(), name = 'contest-delete'),
    path('create/', ContestCreateView.as_view(), name = 'contest-create'),
    path('<int:id>/update/', ContestUpdateView.as_view(), name = 'contest-update'),
]