from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    DetailView, 
    ListView, 
    UpdateView, 
    DeleteView
)

from .forms import ContestModelForm

from .models import Contest

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        return super().form_valid(form)



class ContestUpdateView(UpdateView):
    template_name = "contests/contest_create.html"
    form_class = ContestModelForm
    queryset = Contest.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contest, id = id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)