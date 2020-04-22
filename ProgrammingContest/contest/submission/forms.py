from django import forms

from .models import Submission

grade_choices = [
        ('pass', 'PASS'),
        ('fail', 'FAIL'),
        ('ungraded', 'UNGRADED'),
        ('inprocess', 'INPROCESS')
    ]
language_choices = [
        ('java', 'JAVA'),
        ('c++', 'C++'),
        ('c', 'C'),
        ('python', 'PYTHON'),
        ('c#', 'C#')
    ]


class SubmissionCreateForm(forms.ModelForm):
    submissionLanguage  = forms.ChoiceField(label = "Programming Language", choices = language_choices, initial = "Select ", required = True)
    submissionFile      = forms.FileField(label = "Select a file", required = True)

    class Meta:
        model = Submission
        fields = ['submissionLanguage', 'submissionFile']

class SubmissionGradeForm(forms.ModelForm):
    submissionGrade     = forms.ChoiceField(label = "Grade", choices = grade_choices)
    
    class Meta:
        model = Submission
        fields = ['submissionGrade']