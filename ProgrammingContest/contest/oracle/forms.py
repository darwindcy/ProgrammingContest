from django import forms

from .models import OraclePost


class OraclePostForm(forms.ModelForm):
    postQuestion        = forms.CharField(label = "Question", widget = forms.Textarea, max_length = 500)
    # postUser            = forms.CharField(label = "UserName")
    class Meta:
        model = OraclePost
        fields = [
            'postQuestion',
            
        ]