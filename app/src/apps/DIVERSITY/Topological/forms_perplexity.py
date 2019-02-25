from django import forms
from multiselectfield import MultiSelectField

from .models import Input

class InputForm(forms.ModelForm):
    # dataset = forms.MultipleChoiceField(choices=dataset_options, widget=forms.CheckboxSelectMultiple())
    # peptide_type = forms.MultipleChoiceField(choices=peptide_type_options, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Input        
        fields = ("perplexity",)  
