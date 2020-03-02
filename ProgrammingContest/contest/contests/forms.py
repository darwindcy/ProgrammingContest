from django import forms

from .models import Contest

from users.models import CustomUser

class DateInput(forms.DateInput):
    input_type = 'date'

class ContestUpdateForm(forms.ModelForm):
    contestName         = forms.CharField(label = "Contest Name")
    contestDate         = forms.DateField(label = "Date", widget = DateInput)
    contestants         = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
        queryset = CustomUser.objects.all(), required = False)

    contestHours        = forms.IntegerField(label = "Hours", min_value = 0, required = True)
    contestMinutes      = forms.IntegerField(label = "Minutes", min_value = 0, required = True)

    class Meta:
        model = Contest
        fields = [
            'contestName',
            'contestDate',
            'contestants', 
            'contestHours',
            'contestMinutes',
        ]
        labels = {'contestHours: Contest Hours', 'contestMinutes : Contest Minutes'}

class ContestModelForm(forms.ModelForm):
    contestName         = forms.CharField(label = "Contest Name")
    contestDate         = forms.DateField(label = "Date", widget = DateInput)
    #contestants = forms.MultipleChoiceField(label = "Contestants",
     #                   widget = forms.CheckboxSelectMultiple,
      #                  choices = Contest.contestants.all())
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
            'contestMinutes'
        ]
        labels = {'contestHours: Contest Hours', 'contestMinutes : Contest Minutes'}
        # add validation by def clean_title ... example