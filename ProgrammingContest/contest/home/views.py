from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from contests.models import Contest
        running_contests = Contest.objects.filter(isRunning = True)

        context['runningContests'] = running_contests

        return context