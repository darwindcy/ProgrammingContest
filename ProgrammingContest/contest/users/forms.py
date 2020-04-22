from django import forms

from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


user_choices  = [
    ('administrator', 'ADMINISTRATOR'),
    ('team', 'TEAM'),
    ('grader', 'GRADER'),
]

class UserModelForm(forms.ModelForm):
    userNameDetail = forms.CharField(label = "Name", required = False)
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)
    userType = forms.ChoiceField(label = "User Type", choices = user_choices, required = True)

    from contests.models import Contest
    participatingIn = forms.ModelMultipleChoiceField(label = "Participating In", widget = forms.CheckboxSelectMultiple, queryset = Contest.objects.all(), required = False)

    class Meta:
        model = CustomUser
        fields = ('userNameDetail', 'userName', 'password', 'userType', 'participatingIn')
    
    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        qs = CustomUser.objects.filter(userName = userName)
        if qs.exists():
            raise forms.ValidationError("User already present")
        return userName

    # add validation by def clean_title ... example
    def save(self, commit = True):
        user = super(UserModelForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    userType = forms.ChoiceField(label = "User Type", choices = user_choices, required = True)
    
    from contests.models import Contest
    participatingIn = forms.ModelMultipleChoiceField(label = "Participating In", widget = forms.CheckboxSelectMultiple, queryset = Contest.objects.all(), required = False)

    class Meta: 
        model = CustomUser
        fields = ('userName', 'userType', 'participatingIn')

    def clean_password(self):
        return self.initial("password")



class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'userName',
            'password',
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
        model = CustomUser
        fields = ('userName', 'password', 'userType', 'participatingIn')
    
    
    def clean_password(self):
        return self.initial("password")
