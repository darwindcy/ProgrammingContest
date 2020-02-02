from django.urls import path

from .views import(
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name = 'user-list'),
    path('<int:id>/', UserDetailView.as_view(), name = 'user-detail'),
    path('create/', UserCreateView.as_view(), name = 'user-create'),
    path('<int:id>/update/', UserUpdateView.as_view(), name = 'user-update'),
    path('<int:id>/delete/', UserDeleteView.as_view(), name = 'user-delete'),
]