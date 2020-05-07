"""contest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from users.views import random_view

from home.views import HomePageView

from django.contrib.auth.decorators import login_required

# Base for all the urls, the app urls are included here
urlpatterns = [
    path('', HomePageView.as_view()),

    path('submission/', include('submission.urls')),

    path('home/', include('home.urls')),
    
    path('oracle/', include('oracle.urls')),

    path('login/', include('login.urls')),

    path('users/', include('users.urls')),

    path('contests/', include('contests.urls')),

    path('users/random/', random_view),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)