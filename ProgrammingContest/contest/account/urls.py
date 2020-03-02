from django.urls import path

app_name = 'account'

from .views import Accountpageview, AdminAccountView, GraderAccountView, TeamAccountView

urlpatterns = [
    path('', Accountpageview.as_view(), name = 'account-view'),
    path('admin/', AdminAccountView.as_view(), name = 'admin-acc-view'),
    path('grader/', GraderAccountView.as_view(), name = 'grader-acc-view'),
    path('team/', TeamAccountView.as_view(), name = 'team-acc-view')
]