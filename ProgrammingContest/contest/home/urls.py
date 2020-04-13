from django.urls import path

app_name = 'home'

from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name = 'homepage-view')
]