from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import(
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('', login_required(UserListView.as_view()), name = 'user-list'),
    path('<int:id>/', login_required(UserDetailView.as_view()), name = 'user-detail'),
    path('create/', login_required(UserCreateView.as_view()), name = 'user-create'),
    path('<int:id>/update/', login_required(UserUpdateView.as_view()), name = 'user-update'),
    path('<int:id>/delete/', login_required(UserDeleteView.as_view()), name = 'user-delete'),
]