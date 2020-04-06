from django import forms

from .models import OraclePost

class OraclePostForm(forms.ModelForm):
    postQuestion        = forms.CharField(label = "Question", widget = forms.Textarea, max_length = 500)
    #postUser            = forms.CharField(label = "User Name", required = False, disabled = True)
    
    class Meta:
        model = OraclePost
        fields = [
            'postQuestion',
        ]
    
class OracleUpdateForm(forms.ModelForm):
    postQuestion        = forms.CharField(label = "Question", widget = forms.Textarea, disabled = True)
    postAnswer          = forms.CharField(label = "Answer", widget = forms.Textarea, max_length = 500)
    #postAnswerer        = forms.CharField(label = "Answered By", disabled = True)

    class Meta:
        model = OraclePost
        fields = [
            'postQuestion', 'postAnswer',
        ]