from django.db import models
from django import forms
from multiselectfield import MultiSelectField

amino_first_options = (
        ("L-ALA", "L-ALA"),
        ("L-CYS", "L-CYS"),
        ("L-ASP", "L-ASP"),
        ("L-GLU", "L-GLU"),
        ("L-PHE", "L-PHE"),
        ("L-HIS", "L-HIS"),
        ("L-ILE", "L-ILE"),
        ("L-LYS", "L-LYS"),
        ("L-LEU", "L-LEU"),
        ("L-MET", "L-MET"),
        ("L-ASN", "L-ASN"),
        ("L-PRO", "L-PRO"),
        ("L-GLN", "L-GLN"),
        ("L-ARG", "L-ARG"),
        ("L-SER", "L-SER"),
        ("L-THR", "L-THR"),
        ("L-VAL", "L-VAL"),
        ("L-TRP", "L-TRP"),
        ("L-TYR", "L-TYR"),
        ("GLY", "GLY"),
        )
dataset_options = (
        ("L-ALA", "L-ALA"),
        ("L-CYS", "L-CYS"),
        ("L-ASP", "L-ASP"),
        ("L-GLU", "L-GLU"),
        ("L-PHE", "L-PHE"),
        ("L-HIS", "L-HIS"),
        ("L-ILE", "L-ILE"),
        ("L-LYS", "L-LYS"),
        ("L-LEU", "L-LEU"),
        ("L-MET", "L-MET"),
        ("L-ASN", "L-ASN"),
        ("L-PRO", "L-PRO"),
        ("L-GLN", "L-GLN"),
        ("L-ARG", "L-ARG"),
        ("L-SER", "L-SER"),
        ("L-THR", "L-THR"),
        ("L-VAL", "L-VAL"),
        ("L-TRP", "L-TRP"),
        ("L-TYR", "L-TYR"),
        ("GLY", "GLY"),
        )

peptide_type_options = (
        ('LIN NM', 'Linear N-Methylated'),
        ('LIN', 'Linear'),
        ('CYC', 'Cyclic'),
        ('CYC NM', 'Cyclic N-Methylated')
)

class Input(models.Model):

    amino_first = MultiSelectField(verbose_name="First Position", choices=amino_first_options, max_choices=1)
    dataset = MultiSelectField(verbose_name="Dataset", choices=dataset_options, max_choices=20)
    peptide_type = MultiSelectField(verbose_name="Peptide Length", choices=peptide_type_options, max_choices=4)
    peptide_length = models.FloatField(verbose_name="Peptide length" , default = 2)
