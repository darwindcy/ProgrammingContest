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

from .forms import UserModelForm, UserAdminCreationForm, UserAdminUpdateForm, UserUpdateForm

from .models import CustomUser

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class UserListView(ListView):
    template_name = 'users/user_list.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    queryset = CustomUser.objects.all()

class UserDetailView(DetailView):
    template_name = 'users/user_detail.html'
    queryset = CustomUser.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CustomUser, id = id_)

class UserCreateView(CreateView):
    model = CustomUser
    template_name = "users/user_create.html"
    form_class = UserModelForm
    queryset = CustomUser.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        
        participatingIn = form.cleaned_data['participatingIn']
        form.instance.save()

        from contests.models import Contest
        participating_list = Contest.objects.filter(pk__in = participatingIn)
        for ins in participating_list:
            ins.contestants.add(form.instance)
            print(ins)
            form.instance.participatingIn.add(ins)

        return super().form_valid(form)

class UserUpdateView(UpdateView):
    template_name = "users/user_update.html"
    form_class = UserUpdateForm
    queryset = CustomUser.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CustomUser, id = id_)

    def form_valid(self, form):
        participatingIn = form.cleaned_data['participatingIn']
        id_ = self.kwargs.get("id")

        from contests.models import Contest
        print("current user")
        current_user = CustomUser.objects.get(id = id_)
        print(current_user)
        
        previous_list = Contest.objects.filter(contestants__id = id_) 
        print("Previous List")
        print(previous_list)
        participating_list = Contest.objects.filter(pk__in = participatingIn)
        print(participating_list)

        for instance in previous_list:
            instance.contestants.remove(current_user)

        for instance in participating_list:
            instance.contestants.add(current_user)

        print(form.cleaned_data)
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    template_name = 'users/user_delete.html'
    #queryset = User.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CustomUser, id = id_)
    
    def get_success_url(self):
        return reverse('users:user-list')

def random_view(request, *args, **kwargs):
    return render(request, "random_page.html", {})