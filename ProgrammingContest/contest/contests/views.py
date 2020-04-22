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
from contest.decorators import class_view_decorator, admin_only_view, custom_login_required, admin_grader_only
from django.contrib import messages

import os, shutil
import datetime
from collections import OrderedDict

@class_view_decorator(custom_login_required)
class ContestProblemCreateView(CreateView):
    model = Problem
    template_name  = "contests/problem_create.html"
    form_class = ProblemCreateForm
    queryset = Problem.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        id_ = self.kwargs.get("id")
        form.instance.contest = Contest.objects.get(id = id_)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('contests:contest-list')

@class_view_decorator(custom_login_required)
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
        context['contest']          = current_contest
        score_data = {}

        for team in teams:
            score_data[team] = {}
            sum = 0
            correct_submissions = 0
            for problem in problem_list:
                submissions_of_problem_for_team = submissionList.filter(submissionTeam = team, submissionProblem = problem)
                if submissions_of_problem_for_team.count() > 0:
                    #print("sub list", submissions_of_problem_for_team)
                    #print("sub list", submissions_of_problem_for_team.order_by('-subTouchTime'))
                    
                    main_submission = submissions_of_problem_for_team.order_by('-subTouchTime').first()
                    print("Main Submission", main_submission)
                    if main_submission.submissionGrade == "pass":
                        correct_submissions += 1
                    score_data[team][problem] = main_submission
                    sum += main_submission.get_submission_score()
                
            score_data[team]["sum"] = sum
            score_data[team]["correct"] = correct_submissions
        
        
        context['score_data'] = score_data
       
        
        od = OrderedDict(sorted (score_data.items(), key = lambda kv:kv[1]["sum"], reverse=False))
        od = OrderedDict(sorted (score_data.items(), key = lambda kv:kv[1]["correct"], reverse=True))

        context['score_data'] = od

        remainingTime = current_contest.get_remaining_time()
        
        if (remainingTime.seconds // 3600 > 0 or ((remainingTime.seconds // 60) % 60) >= 30 or (remainingTime.seconds == 0)): 
            scoreboard_active = True
        else:
            scoreboard_active = False
        context['active_status'] = scoreboard_active
        return context

@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class ContestSubmissionsListView(ListView):
    template_name = "contests/contest_submissions.html"
    
    def get_queryset(self):
        from submission.models import Submission
        contest_id       = self.kwargs.get("id")
        current_contest     = Contest.objects.get(id = contest_id)
        problem_list        = current_contest.contestproblems.all()
        submissionList      = Submission.objects.filter(submissionProblem__in = problem_list)
        latestSubmissions   = []

        for eachuser in current_contest.contestants.all():
            submissions = submissionList.filter(submissionTeam = eachuser)
            for each_problem in problem_list:
                all_submissions = submissions.filter(submissionProblem = each_problem)
                if all_submissions.count() > 0:
                    main_submission = all_submissions.order_by('-subTouchTime').first()
                    latestSubmissions.append(main_submission)

        return latestSubmissions

@class_view_decorator(custom_login_required)
class ContestSubmissionsForTeamView(ListView):
    template_name = "contests/contest_submissions_for_team.html"
    
    def get_queryset(self):
        from submission.models import Submission
        contest_id       = self.kwargs.get("id")
        team_id          = self.kwargs.get("team_id")
        current_contest     = Contest.objects.get(id = contest_id)
        problem_list        = current_contest.contestproblems.all()

        submissionList      = Submission.objects.filter(submissionProblem__in = problem_list)
        from users.models import CustomUser
        print("selected user", CustomUser.objects.get(id = team_id))
        teamSubmissionList  = submissionList.filter(submissionTeam = CustomUser.objects.get(id = team_id))
        print("team submission list", teamSubmissionList)
        return teamSubmissionList

@class_view_decorator(custom_login_required)
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        id_problem = self.kwargs.get("problem_id")

        from submission.models import Submission
        qs = Submission.objects.filter(submissionTeam = self.request.user, submissionProblem = Problem.objects.get(id = id_problem))
        
        if qs.exists:
            for ins in qs:
                currSubmission = ins
                context['currSubmission'] = currSubmission
        
        
        return context

@class_view_decorator(custom_login_required)
class ContestListView(ListView):
    template_name = "contests/contest_list.html"

    def get_queryset(self):
        if(self.request.user.userType.lower() == "team"):
            return Contest.objects.all().filter(contestants = self.request.user)
        else:
            return Contest.objects.all()
            

@class_view_decorator(custom_login_required)
class ContestStartView(TemplateView):
    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        if Contest.objects.get(id = id_).isRunning == False:
            if(Contest.objects.get(id = id_).isPaused == True):  
                messages.success(request, 'Contest Resumed')
            else:
                messages.success(request, 'Contest Successfully Started')
            Contest.objects.filter(id = id_).update(isRunning = True)
            currentTime = datetime.datetime.now().time()
            Contest.objects.filter(id = id_).update(startTime = currentTime)
        else:
            messages.success(request, 'Contest already running, Cannot start again')
        return ContestListView.as_view()(self.request)    

@class_view_decorator(custom_login_required)
class ContestPauseView(TemplateView):
    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        if Contest.objects.get(id = id_).isRunning == True:

            print('Time remaining', Contest.objects.get(id = id_).get_remaining_time())
            Contest.objects.filter(id = id_).update(contestDuration = Contest.objects.get(id = id_).get_remaining_time())

            Contest.objects.filter(id = id_).update(isRunning = False)
            Contest.objects.filter(id = id_).update(isPaused = True)
            messages.success(request, 'Contest Successfully Paused')
        else:
            messages.success(request, 'Contest not running')
        return ContestListView.as_view()(self.request)

@class_view_decorator(custom_login_required)
class ContestStopView(TemplateView):
    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        current_contest = Contest.objects.get(id = id_)

        if current_contest.isRunning == True or current_contest.isPaused:
            Contest.objects.filter(id = id_).update(isRunning = False)
            Contest.objects.filter(id = id_).update(isPaused = False)

            currentTime = datetime.datetime.now().time()
            
            Contest.objects.filter(id = id_).update(stopTime = currentTime)
            Contest.objects.filter(id = id_).update(pauseTime = None)
            Contest.objects.filter(id = id_).update(contestDuration = datetime.timedelta(seconds = (
                                                    current_contest.contestHours*60 + current_contest.contestMinutes)*60))
            messages.success(request, 'Contest Successfully Stopped')
        else:
            messages.success(request, 'Contest already stopped')
        return ContestListView.as_view()(self.request)    

@class_view_decorator(custom_login_required)
class ContestDetailView(DetailView):
    template_name = 'contests/contest_detail.html'
    queryset = Contest.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)


@class_view_decorator(custom_login_required)
class ContestDeleteView(DeleteView):
    template_name = 'contests/contest_delete.html'
    #queryset = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        current_contest = Contest.objects.get(id = id_)
        problem_list        = current_contest.contestproblems.all()

        from submission.models import Submission
        submissionList      = Submission.objects.filter(submissionProblem__in = problem_list)
        for each in submissionList:
            each.delete()
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        path = os.path.join(media_root,"submissions", current_contest.contestName)
       
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        return get_object_or_404(Contest, id = id_)
        
    
    def get_success_url(self):
        return reverse('contests:contest-list')

@class_view_decorator(custom_login_required)
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

@class_view_decorator(custom_login_required)
class ContestUpdateView(UpdateView):
    template_name = "contests/contest_update.html"
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