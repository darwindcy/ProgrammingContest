from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def access_required(allowed_users=[]):
    def decorator(func):
        def send(request, *args, **kwargs):
            if request.role in allowed_users:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return send
    return decorator

def custom_login_required(myFunc):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return myFunc(request, *args, **kwargs)
        else:
            messages.success(request, 'You are not logged in')
            messages.success(request, 'Please log-in to continue')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return wrap

def class_view_decorator(function_decorator):
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

def admin_only_view(myFunc):
    def wrap(request, *args, **kwargs):
        if request.user.userType.lower() == "administrator":
            return myFunc(request, *args, **kwargs)
        else:
            messages.success(request, 'You dont have access to this page.')
            messages.success(request, 'Contact the administrator for access to this page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return wrap

def grader_only_view(myFunc):
    def wrap(request, *args, **kwargs):
        if request.user.userType.lower() == "grader":
            return myFunc(request, *args, **kwargs)
        else:
            messages.success(request, 'You dont have access to this page.')
            messages.success(request, 'Contact the administrator for access to this page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return wrap

def admin_grader_only(myFunc):
    def wrap(request, *args, **kwargs):
        if request.user.userType.lower() == "grader" or request.user.userType == "administrator":
            return myFunc(request, *args, **kwargs)
        else:
            messages.success(request, 'You dont have access to this page.')
            messages.success(request, 'Contact the administrator for access to this page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return wrap