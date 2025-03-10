from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    ListView, 
    DetailView,
    UpdateView, 
    DeleteView
)

#from .forms import OracelPostForm

from .models import OraclePost

from .forms import OraclePostForm, OracleUpdateForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from contest.decorators import class_view_decorator, custom_login_required, admin_only_view, admin_grader_only

# Create your views here.

@class_view_decorator(custom_login_required)
class PostsListView(ListView):
    template_name = "oracle/oracle_posts_list.html"
    queryset = OraclePost.objects.all()

@class_view_decorator(custom_login_required)
class PostCreateView(CreateView):
    template_name = "oracle/new_post.html"
    form_class = OraclePostForm
    queryset = OraclePost.objects.all()

    def form_valid(self, form):
        form.instance.postUser = self.request.user
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('oracle:posts-list')

@class_view_decorator(custom_login_required)
class PostDetailView(DetailView):
    template_name = 'oracle/detail_post.html'
    queryset = OraclePost.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)
        
@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class PostAnswerView(UpdateView):
    template_name = 'oracle/answer_post.html'
    form_class = OracleUpdateForm
    queryset = OraclePost.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)

    def form_valid(self, form):
        form.instance.postAnswerer = self.request.user
        form.instance.isAnswered = True
        print(form.cleaned_data)
        return super().form_valid(form)

@class_view_decorator(custom_login_required)
@class_view_decorator(admin_grader_only)
class PostDeleteView(DeleteView):
    template_name = 'oracle/delete_post.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)
    
    def get_success_url(self):
        return reverse('oracle:posts-list')

