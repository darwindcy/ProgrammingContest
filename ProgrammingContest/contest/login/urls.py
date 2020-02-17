from django.urls import path

from .views import (
    LoginPageView,
    SampleView,
    LogoutView,
    UnloggedPageView,
)

app_name = 'login'

urlpatterns = [
    path('', LoginPageView.as_view(), name='login-page'),
    path('sample', SampleView.as_view(), name='sample'),
    path('logout', LogoutView.as_view(), name='logout-page'),
    path('unlogged', UnloggedPageView.as_view(), name = 'unlogged-page'),
]