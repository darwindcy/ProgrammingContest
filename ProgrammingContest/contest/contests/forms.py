from django import forms

from .models import Contest

class DateInput(forms.DateInput):
    input_type = 'date'

class ContestModelForm(forms.ModelForm):
    contestName = forms.CharField(label = "Contest Name")
    contestDate = forms.DateField(label = "Date", widget = DateInput)
    contestParticipants = forms.CharField(label = "Participants")
    
    class Meta:
        model = Contest
        fields = [
            'contestName',
            'contestDate',
            'contestParticipants',
        ]

        # add validation by def clean_title ... example