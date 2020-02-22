from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.views.generic import(
    CreateView, 
    DetailView, 
    ListView, 
    UpdateView, 
    DeleteView
)
# Create your views here.

from .forms import UserModelForm, UserAdminCreationForm, UserAdminUpdateForm

from .models import customUser

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class UserListView(ListView):
    template_name = 'users/user_list.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    queryset = customUser.objects.all()

class UserDetailView(DetailView):
    template_name = 'users/user_detail.html'
    queryset = customUser.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(customUser, id = id_)

class UserCreateView(CreateView):
    template_name = "users/user_create.html"
    form_class = UserAdminUpdateForm
    queryset = customUser.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    template_name = "users/user_create.html"
    form_class = UserModelForm
    queryset = customUser.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(customUser, id = id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    template_name = 'users/user_delete.html'
    #queryset = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(customUser, id = id_)
    
    def get_success_url(self):
        return reverse('users:user-list')

def random_view(request, *args, **kwargs):
    return render(request, "random_page.html", {})