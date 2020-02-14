from django import forms

from .models import User

user_choices  = [
    ('administrator', 'ADMINISTRATOR'),
    ('participant', 'PARTICIPANT'),
    ('grader', 'GRADER'),
]

class UserModelForm(forms.ModelForm):
    userName = forms.CharField(label = "User Name")
    userType = forms.ChoiceField(label = "User Type", choices = user_choices, required = True)
    password = forms.CharField(label = "Password")
    
    from contests.models import Contest
    participatingIn = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset = Contest.objects.all())

    class Meta:
        model = User
        fields = [
            'userName',
            'userType',
            'password',
            'participatingIn',
        ]
        # add validation by def clean_title ... example