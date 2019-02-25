from django.db import models
from django import forms
from multiselectfield import MultiSelectField

class Input(models.Model):

    perplexity = models.FloatField(verbose_name="Perplexity" , default = 50)