from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    DetailView, 
    ListView, 
    UpdateView, 
    DeleteView
)

from .forms import ContestModelForm, ContestUpdateForm

from .models import Contest

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime

class ContestListView(ListView):
    template_name = "contests/contest_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    queryset = Contest.objects.all()

class ContestDetailView(DetailView):
    template_name = 'contests/contest_detail.html'
    queryset = Contest.objects.all()

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