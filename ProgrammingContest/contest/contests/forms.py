from django import forms

from .models import Contest

from users.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class ContestModelForm(forms.ModelForm):
    contestName = forms.CharField(label = "Contest Name")
    contestDate = forms.DateField(label = "Date", widget = DateInput)
    contestParticipants = forms.CharField(label = "Participants")
    #contestants = forms.MultipleChoiceField(label = "Contestants",
     #                   widget = forms.CheckboxSelectMultiple,
      #                  choices = Contest.contestants.all())
    contestants = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
        queryset = User.objects.all())
    class Meta:
        model = Contest
        fields = [
            'contestName',
            'contestDate',
            'contestParticipants',
            'contestants'
        ]

        # add validation by def clean_title ... example