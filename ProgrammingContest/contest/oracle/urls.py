from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import (
    PostsListView,
    PostCreateView,
    PostDetailView,
    PostAnswerView,
    PostDeleteView
)

app_name = 'oracle'

urlpatterns = [
    path('', PostsListView.as_view(), name='posts-list'),
    path('create/', PostCreateView.as_view(), name = 'post-create'),
    path('<int:id>/', PostDetailView.as_view(), name = 'post-detail'),
    path('<int:id>/answer/', PostAnswerView.as_view(), name = 'post-answer'),
    path('<int:id>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
]