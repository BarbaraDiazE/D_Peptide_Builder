from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
from .forms import InputForm
from .compute_sequence import ComputeSequence
from apps.PCA.compute_pca import GeneratePCA


class ServerViews(APIView):

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            letters = form.cleaned_data.get('picked')
            form = form.save(commit=False)
            form.save()
            # return present_output(form)
            amino_first = form.amino_first
            dataset = form.dataset
            peptide_type = form.peptide_type
            peptide_length = str(round(form.peptide_length))

            cs = ComputeSequence(amino_first, dataset, peptide_type, peptide_length)
            Database = cs.generate_dataframe()
            smile_lin, smile_lin_nm, smile_cyc, smile_cyc_nm = cs.get_smiles()

            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'database_{now}.csv'
            route = f'generated_csv/{filename}'

            request.session['csv_name'] = filename

            save_lists(smile_lin, f'smile_lin_{filename}.pkl')
            save_lists(smile_lin_nm, f'smile_lin_nm_{filename}.pkl')
            save_lists(smile_cyc, f'smile_cyc_{filename}.pkl')
            save_lists(smile_cyc_nm, f'smile_cyc_nm_{filename}.pkl')

            download_csv = Database.to_csv(route, encoding='utf-8', index = True)
            return redirect(f'/csv/{filename}/')
        return render(request,'home.html',{'form': form})

    def get(self, request):
        form = InputForm()
        return render(request,'home.html',{'form': form})


class CSVView(APIView):
    def get(self, request, csv_name):
        data = pd.read_csv(f'generated_csv/{csv_name}')
        data_html = data.to_html()
        context = {'loaded_data': data_html}
        return render(request, 'table.html', context)


class DownloadCSV(APIView):
    def get(self, request):
        csv_name = request.session['csv_name']
        filename = f'generated_csv/{csv_name}'
        with open(filename, 'rb') as csv_file:
            response = HttpResponse(csv_file, content_type="text/csv")
            response['Content-Disposition'] = f'attachment; filename = {filename}'
            return response


def save_lists(itemlist, filename):
    with open('pickles/' + filename, 'wb') as fp:
        pickle.dump(itemlist, fp)