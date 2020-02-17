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

from .forms import OraclePostForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class PostsListView(ListView):
    
    template_name = "oracle/oracle_posts_list.html"
    queryset = OraclePost.objects.all()

class PostCreateView(CreateView):
    model = OraclePost
    template_name = "oracle/new_post.html"
    form_class = OraclePostForm
    queryset = OraclePost.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('oracle:posts-list')

class PostDetailView(DetailView):
    template_name = 'oracle/detail_post.html'
    queryset = OraclePost.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)

class PostAnswerView(DetailView):
    template_name = "oracle/answer_post.html"
    queryset = OraclePost.objects.all()
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)

class PostDeleteView(DeleteView):
    template_name = 'oracle/delete_post.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(OraclePost, id = id_)
    
    def get_success_url(self):
        return reverse('oracle:posts-list')

