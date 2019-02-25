from django import forms
from multiselectfield import MultiSelectField

from .models import Input

class InputForm(forms.ModelForm):
    class Meta:
        model = Input        
        fields = ("perplexity",)  