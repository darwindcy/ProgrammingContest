from django.urls import path

from .views import (
    LoginPageView,
    LogoutView,
)

app_name = 'login'

urlpatterns = [
    path('', LoginPageView.as_view(), name='login-page'),
    path('logout', LogoutView.as_view(), name='logout-page'),
]