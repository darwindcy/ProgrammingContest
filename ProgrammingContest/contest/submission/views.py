from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy

import datetime

from django.views.generic import(
    CreateView, 
    ListView, 
    UpdateView,
    DetailView
)

from .models import Submission

from .forms import SubmissionCreateForm, SubmissionGradeForm
from contest.decorators import class_view_decorator, custom_login_required, admin_only_view, admin_grader_only
from django.contrib import messages

@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class SubmissionListView(ListView):
    template_name = "submission/submission_list.html"

    #queryset = Submission.objects.all()
    def get_queryset(self):
        if(self.request.user.userType.lower() == "administrator" or self.request.user.userType.lower() == "grader"):
            queryset = Submission.objects.all()
        elif(self.request.user.userType.lower() == "team"):
            queryset = Submission.objects.filter(submissionTeam = self.request.user)
        return queryset

@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class SubmissionDownloadView(DetailView):
    template_name = "submission/submission_download.html"
    queryset = Submission.objects.all()
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        obj = Submission.objects.get(id = id_)

        print(obj.submissionGrade)
        return obj

@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class SubmissionGradeView(UpdateView):
    template_name = "submission/submission_grade.html"
    form_class    = SubmissionGradeForm
    queryset      = Submission.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Submission, id = id_)
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def get_success_url(self):
        id_ = self.kwargs.get("id")
        submission = Submission.objects.get(id = id_)
        contest_id = submission.submissionProblem.contest.id
        return reverse('contests:contest-submissions', kwargs={'id':contest_id})

@class_view_decorator(custom_login_required)
class SubmissionCreateView(CreateView):
    template_name = "submission/submission_create.html"
    queryset = Submission.objects.all()
    #fields = ['submissionFile']
    form_class = SubmissionCreateForm

    def form_valid(self, form):
        id_problem = self.kwargs.get('problem_id')
        print(id_problem)
        form.instance.submissionName        =  form.instance.submissionFile.name
        form.instance.submissionTime        =  datetime.datetime.now().time()
        form.instance.submissionTeam        =  self.request.user
        form.instance.submissionGrade       =  "ungraded"
        from contests.models import Problem
        form.instance.submissionProblem     =  Problem.objects.get(id = id_problem)

        print("/*------------------------Hello world----------------------*/")
        form.instance.totalSubmissionCount = does_exist(self)
        print("Total Submissions = " + repr(form.instance.totalSubmissionCount))

        print(form.instance.submissionTime)
        print(form.instance.submissionFile.name)
        print(form.instance.submissionProblem.problemName)

        qs = Submission.objects.filter(submissionTeam = self.request.user, submissionProblem = Problem.objects.get(id = id_problem))
        if qs.exists():
            if (qs.last().submissionGrade.lower() == "pass"):
                messages.success(self.request, "Your previous submission is already accepted. Current submission discarded")
                return super().form_invalid(form)            
        
        return super().form_valid(form)
    
    
    def get_success_url(self):
        if(self.request.user.userType.lower() == "team"):
            id_contest = self.kwargs.get("id")
            id_problem = self.kwargs.get("problem_id")

            return reverse('contests:problem-detail', kwargs = {'id':id_contest, 'problem_id':id_problem})
        return reverse('submission:submission-list')

def does_exist(self):
    from contests.models import Problem
    from users.models import CustomUser

    problem_id  = self.kwargs.get("problem_id")
    qs = Submission.objects.filter(submissionTeam = self.request.user, submissionProblem = Problem.objects.get(id = problem_id))
    submissionCount = 0
    if qs.exists():
        for instance in qs:
            submissionCount = instance.totalSubmissionCount + 1
    else:
        submissionCount = 1
    
    return submissionCount
