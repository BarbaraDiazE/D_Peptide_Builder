
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.template import RequestContext
from rest_framework.views import APIView
from rest_pandas import PandasView
from datetime import datetime

import pandas as pd
import numpy as np
import pickle
import os
import glob
import csv

from .forms_perplexity import InputForm
from .compute_tsne import GenerateTSNE

from bokeh.embed import components

class TSNEatomView(APIView):

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            letters = form.cleaned_data.get('picked')
            form = form.save(commit=False)
            form.save()
            perplexity = int(round(form.perplexity))
            csv_name = request.session['csv_name']

            tsne = GenerateTSNE(csv_name, perplexity)
            plot = tsne.resolve()
            script, div = components(plot)
            return render_to_response('plot_TSNE.html', {'script': script, 'div': div})
        return render(request,'homeperplexity.html',{'form': form})

    def get(self, request):
        form = InputForm()
        return render(request,'homeperplexity.html',{'form': form})