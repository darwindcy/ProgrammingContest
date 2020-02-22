from django import forms

from .models import customUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


user_choices  = [
    ('administrator', 'ADMINISTRATOR'),
    ('team', 'TEAM'),
    ('grader', 'GRADER'),
]

class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = customUser
        fields = [
            'userName',
            'userType',
            'participatingIn',
        ]
    
    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        qs = customUser.objects.filter(userName = userName)
        if qs.exists():
            raise forms.ValidationError("User already present")
        return userName

    userType = forms.ChoiceField(label = "User Type", choices = user_choices, required = True)
    
    from contests.models import Contest
    participatingIn = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset = Contest.objects.all(), required = False)


        # add validation by def clean_title ... example

class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)

    class Meta:
        model = customUser
        fields = [
            'userName',
            'userType',
            'participatingIn',
        ]
    
    def save(self, commit = True):
        user = super(UserAdminCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta: 
        model = customUser
        fields = ('userName', 'password', 'userType', 'participatingIn')
    
    def clean_password(self):
        return self.intitial("password")
