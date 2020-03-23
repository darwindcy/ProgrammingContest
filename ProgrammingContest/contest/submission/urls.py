from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import (
    SubmissionCreateView,
    SubmissionListView,
    SubmissionGradeView,
    SubmissionDownloadView
)

app_name = 'submission'

urlpatterns = [
    path('', SubmissionListView.as_view(), name='submission-list'),
    path('create/', SubmissionCreateView.as_view(), name = 'submission-create'),
    path('<int:id>/grade/', SubmissionGradeView.as_view(), name = 'submission-grade'),
    path('<int:id>/download/', SubmissionDownloadView.as_view(), name = 'submission-download'),
]