from django import forms

from .models import Contest, Problem

from users.models import CustomUser

import datetime
class DateInput(forms.DateInput):
    input_type = 'date'

class ProblemCreateForm(forms.ModelForm):
    problemName         = forms.CharField(label = "Problem Name")
    problemInformation  = forms.CharField(label = "Problem Information", widget = forms.Textarea)
    problemTests        = forms.CharField(label = "ProblemTests", widget = forms.Textarea)
    
    class Meta:
        model = Problem
        fields = [
            
            'problemName',
            'problemInformation',
            'problemTests',
        ]


class ContestUpdateForm(forms.ModelForm):
    contestName         = forms.CharField(label = "Contest Name")
    contestDate         = forms.DateField(label = "Date", widget = DateInput)
    contestants         = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
        queryset = CustomUser.objects.all(), required = False)

    contestHours        = forms.IntegerField(label = "Hours", min_value = 0, required = True)
    contestMinutes      = forms.IntegerField(label = "Minutes", min_value = 0, required = True)
    #contestQuestions    = forms.ModelChoiceField(queryset = Problem.objects.all(), required = False)
    class Meta:
        model = Contest
        fields = [
            'contestName',
            'contestDate',
            'contestants', 
            'contestHours',
            'contestMinutes',
        ]
        labels = {'contestHours: Contest Hours', 'contestMinutes : Contest Minutes', 'contestQuestions : Problems'}

class ContestModelForm(forms.ModelForm):
    contestName         = forms.CharField(label = "Contest Name")
    contestDate         = forms.DateField(label = "Date", widget = DateInput)

    contestants         = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
        queryset = CustomUser.objects.all(), required = False)

    contestHours        = forms.IntegerField(label = "Hours", min_value = 0, required = True)
    contestMinutes      = forms.IntegerField(label = "Minutes", min_value = 0, required = True)


    def clean(self, *args, **kwargs):
        #forms.raiseValidationError("Please Enter a Valid Time")
        contestName     = self.cleaned_data.get("contestName")
        qs = Contest.objects.filter(contestName = contestName)
        if qs.exists():
            raise forms.ValidationError("Another Contest with same name present")
        contestDate     = self.cleaned_data.get("contestDate")
        if(contestDate < datetime.datetime.now().date()):
            raise forms.ValidationError("Today or later Date needed")

        contestHours    = self.cleaned_data.get("contestHours")
        contestMinutes  = self.cleaned_data.get("contestMinutes")
        if(contestHours != 0 or contestMinutes != 0):
            return self.cleaned_data
        else:
            raise forms.ValidationError("Please Enter a Valid Time")

    class Meta:
        model = Contest
        fields = [
            'contestName',
            'contestDate',
            'contestants', 
            'contestHours',
            'contestMinutes',
        ]
        labels = {'contestHours: Contest Hours', 'contestMinutes : Contest Minutes', 'contestQuestions : Problems List'}
        # add validation by def clean_title ... example