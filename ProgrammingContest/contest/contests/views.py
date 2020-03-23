from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    DetailView, 
    ListView, 
    UpdateView, 
    DeleteView,
    TemplateView
)

from .forms import ContestModelForm, ContestUpdateForm, ProblemCreateForm

from .models import Contest, Problem

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import datetime
from collections import OrderedDict

class ContestScoreBoardView(ListView):
    template_name = "contests/contest_scoreboard.html"

    def get_queryset(self):
        contest_id       = self.kwargs.get("id")
        current_contest     = Contest.objects.get(id = contest_id)
        from users.models import CustomUser
        teams = CustomUser.objects.filter(participatingIn = current_contest)
        
        return teams

    def get_team_problem_submission(self, team, problem):
        from submission.models import Submission
        return self.objects.get(submissionTeam = team, submissionProblem = problem)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contest_id       = self.kwargs.get("id")
        current_contest     = Contest.objects.get(id = contest_id)
        problem_list        = current_contest.contestproblems.all()

        from submission.models import Submission
        submissionList      = Submission.objects.filter(submissionProblem__in = problem_list)

        from users.models import CustomUser
        teams = CustomUser.objects.filter(participatingIn = current_contest)

        context['submission_list']  = submissionList
        context['problem_list']     = problem_list
        context['team_list']        = teams
        score_data = {}
        
        for team in teams:
            score_data[team] = {}
            sum = 0
            correct_submissions = 0
            for problem in problem_list:
                for each in submissionList.filter(submissionTeam = team, submissionProblem = problem):
                    if each.submissionGrade == "pass":
                        correct_submissions += 1
                    score_data[team][problem] = each
                    sum += each.get_submission_score()
                
            score_data[team]["sum"] = sum
            score_data[team]["correct"] = correct_submissions
        
        context['score_data'] = score_data
        print("---------------------------------------------Sorted Scores-------------------------------")
        
        od = OrderedDict(sorted (score_data.items(), key = lambda kv:kv[1]["sum"], reverse=False))
        od = OrderedDict(sorted (score_data.items(), key = lambda kv:kv[1]["correct"], reverse=True))

        context['score_data'] = od
            
        print("---------------------------------------------Sorted Scores-------------------------------")

        return context

class ContestSubmissionsListView(ListView):
    template_name = "contests/contest_submissions.html"
    
    def get_queryset(self):
        from submission.models import Submission
        contest_id       = self.kwargs.get("id")
        current_contest     = Contest.objects.get(id = contest_id)
        problem_list        = current_contest.contestproblems.all()

        submissionList      = Submission.objects.filter(submissionProblem__in = problem_list)
        print(problem_list)
        print(submissionList)
        return submissionList

class ProblemDetailView(DetailView):
    template_name = "contests/contest_problem_detail.html"

    def get_queryset(self):
        id_     = self.kwargs.get("id")
        print(id_)
        currObj = Contest.objects.get(id = id_) 
        return currObj.contestproblems.all()
    
    def get_object(self):
        id_problem = self.kwargs.get("problem_id")
        id_        = self.kwargs.get("id")

        currentobj = Contest.objects.get(id = id_)

        currObj    = currentobj.contestproblems.get(id = id_problem)
        return currObj

class ContestListView(ListView):
    template_name = "contests/contest_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    queryset = Contest.objects.all()

class ContestStartView(DetailView):
    queryset = Contest.objects.all()
    #fields = ['isRunning']
    template_name = "contests/contest_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        Contest.objects.filter(id = id_).update(isRunning = True)
        print("current Time")
        
        currentTime = datetime.datetime.now().time()
        print(currentTime)
        Contest.objects.filter(id = id_).update(startTime = currentTime)
        return get_object_or_404(Contest, id = id_)      
    
    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     form.instance.isRunning = True
    #     return super().form_valid(form)

class ContestStopView(DetailView):
    queryset = Contest.objects.all()
    template_name = "contests/contest_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        Contest.objects.filter(id = id_).update(isRunning = False)
        print("stop time current time ")
        currentTime = datetime.datetime.now().time()
        print(currentTime)
        Contest.objects.filter(id = id_).update(stopTime = currentTime)
        return ContestDetailView

class ContestDetailView(DetailView):
    template_name = 'contests/contest_detail.html'
    queryset = Contest.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)

class ContestDetailTeamView(DetailView):
    template_name = 'contests/contest_team_detail.html'
    queryset      = Contest.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)

class ContestDeleteView(DeleteView):
    template_name = 'contests/contest_delete.html'
    #queryset = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)
    
    def get_success_url(self):
        return reverse('contests:contest-list')

class ProblemCreateView(CreateView):
    model = Problem
    template_name  = "contests/problem_create.html"
    form_class = ProblemCreateForm
    queryset = Problem.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('contests:contest-list')

class ContestCreateView(CreateView):
    model = Contest
    template_name = "contests/contest_create.html"
    form_class = ContestModelForm
    queryset = Contest.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        hours       = form.cleaned_data['contestHours']
        minutes     = form.cleaned_data['contestMinutes']
        form.instance.contestDuration = datetime.timedelta(seconds = (hours*60 + minutes)*60)
        contestants = form.cleaned_data['contestants']
        form.instance.save()
        
        from users.models import CustomUser
        participant_list = CustomUser.objects.filter(pk__in = contestants)

        for instance in participant_list:
            instance.participatingIn.add(form.instance)
            form.instance.contestants.add(instance)

        return super().form_valid(form)

class ContestUpdateView(UpdateView):
    template_name = "contests/contest_create.html"
    form_class = ContestUpdateForm
    queryset = Contest.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        hours       = form.cleaned_data['contestHours']
        minutes     = form.cleaned_data['contestMinutes']
        form.instance.contestDuration = datetime.timedelta(seconds = (hours*60 + minutes)*60)
        id_ = self.kwargs.get("id")
        contestants = form.cleaned_data['contestants']

        from users.models import CustomUser
        current_contest = Contest.objects.get(id = id_)

        previous_list   = CustomUser.objects.filter(participatingIn__id = id_)
        
        current_list    = CustomUser.objects.filter(pk__in = contestants)

        for instance in previous_list:
            instance.participatingIn.remove(current_contest)

        for instance in current_list:
            instance.participatingIn.add(current_contest)

        return super().form_valid(form)