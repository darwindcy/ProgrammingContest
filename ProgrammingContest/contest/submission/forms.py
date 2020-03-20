from django import forms

from .models import Submission

grade_choices = [
        ('pass', 'PASS'),
        ('fail', 'FAIL'),
        ('ungraded', 'UNGRADED'),
        ('inprocess', 'INPROCESS')
    ]


class SubmissionCreateForm(forms.ModelForm):
    submissionFile      = forms.FileField(label = "Select a file", required = False)

    class Meta:
        model = Submission
        fields = ['submissionFile']

class SubmissionGradeForm(forms.ModelForm):
    submissionGrade     = forms.ChoiceField(label = "Grade", choices = grade_choices)
    
    class Meta:
        model = Submission
        fields = ['submissionGrade']