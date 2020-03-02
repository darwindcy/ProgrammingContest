from django.urls import path

app_name = 'home'

from .views import Homepageview

urlpatterns = [
    path('', Homepageview.as_view(), name = 'homepage-view')
]