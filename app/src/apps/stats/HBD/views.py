from rest_framework.views import APIView
from django.http import HttpResponse

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

import pandas as pd
import os
import glob

from .compute_HBD import StatHBD

class HBDView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = StatHBD(csv_name)
        stat_hbd_html = stat.resolve()
        context = {'loaded_data': stat_hbd_html}
        return render(request, 'stats.html', context)        