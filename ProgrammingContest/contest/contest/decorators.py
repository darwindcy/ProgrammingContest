from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

def access_required(allowed_users=[]):
    def decorator(func):
        def send(request, *args, **kwargs):
            if request.role in allowed_users:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return send
    return decorator

def view_differentiator(adminView, graderView, teamView):
    def outer_decorator(my_func):
        def inner_decorator(request, *args, **kwargs):
            if request.user.userType.lower() == "administrator":
                template = adminView
            elif request.user.userType.lower() == "grader":
                template = graderView
            else:
                template = teamView
            
            return my_func(request, template)
        return inner_decorator
    return outer_decorator


def admin_only_view(myFunc):
    None

def grader_only_view(myFunc):
    None

def team_only_view(myFunc):
    None