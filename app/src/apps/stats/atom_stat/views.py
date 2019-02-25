from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

import pandas as pd
import os
import glob

from .compute_atom import statATOM

class ATOMView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = statATOM(csv_name)
        stat_atom_html = stat.resolve()
        context = {'loaded_data': stat_atom_html}
        return render(request, 'stats_atom.html', context)