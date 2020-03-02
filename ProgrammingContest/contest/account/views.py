from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView, ListView
from contest.decorators import view_differentiator

from contests.models import Contest

#@view_differentiator("account_admin.html","account_grader.html","account_team.html")

# class Accountpageview(TemplateView):
#     template_name = "account/account_team.html"

class Accountpageview(TemplateView):
    def get(self, request):
        if self.request.user.userType.lower() == "administrator":
            return render(request, 'account/account_admin.html')
        elif self.request.user.userType.lower() == "grader":
            return render(request, 'account/account_grader.html')
        else:
            return render(request, 'account/account_team.html')

class AdminAccountView(TemplateView):
    template_name = "account/account_admin.html"

class GraderAccountView(TemplateView):
    template_name = "account/account_grader.html"

class TeamAccountView(ListView):
    template_name = "account/account_team.html"
    #queryset = Contest.objects.filter(CustomUsers__id__exact = request.user.id)
    # def get_queryset(self):
    #      return Contest.objects.all()
    def get_queryset(self, *args, **kwargs):
        return Contest.objects.all().filter(contestants = self.request.user)



# def template_decider(request):
#     if request.user.userType.lower() == "administrator":
#         return render(request, 'account_admin.html')
#     elif request.user.userType.lower() == "grader":
#         return render(request, 'account_grader.html')
#     else:
#         return render(request, 'account_team.html')

# def template_decider(request):
#     if request.user.userType.lower() == "administrator":
#         return render(request, 'account_admin.html')
#     elif request.user.userType.lower() == "grader":
#         return render(request, 'account_grader.html')
#     else:
#         return render(request, 'account_team.html')