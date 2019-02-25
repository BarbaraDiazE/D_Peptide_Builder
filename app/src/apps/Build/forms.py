from django import forms
from multiselectfield import MultiSelectField

from .models import Input, dataset_options, peptide_type_options

class InputForm(forms.ModelForm):
    dataset = forms.MultipleChoiceField(choices=dataset_options, widget=forms.CheckboxSelectMultiple())
    peptide_type = forms.MultipleChoiceField(choices=peptide_type_options, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Input        
        fields = ("amino_first", "dataset", "peptide_type", "peptide_length")  
