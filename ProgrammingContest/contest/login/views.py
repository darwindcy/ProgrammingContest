from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView

from contests.models import Contest

# Create your views here.

class SampleView(TemplateView):
    template_name = "login/sample.html"

class UnloggedPageView(TemplateView):
    template_name = "login/unlogged_page.html"

class LoginPageView(FormView):
    template_name = "login/login_page2.html"
    success_url = '/account'
    form_class = AuthenticationForm

    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginPageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginPageView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        
        if self.request.user.userType.lower() == "administrator":
            redirect_to = '/account/admin/'
        elif self.request.user.userType.lower() == "grader":
            redirect_to = '/account/grader/'
        else:
            redirect_to = '/account/team/'
        
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


    