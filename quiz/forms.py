from django import forms
from .models import Test

class QuestionsAddForm(forms.Form):
    questions = forms.CharField(widget = forms.Textarea(attrs={'rows':25, 'cols':40, 'class':'form-control'}))