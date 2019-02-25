from rest_framework.views import APIView
from django.http import HttpResponse
#ESTO ES NUEVO
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

import pandas as pd
import os
import glob

from .compute_HBA import StatHBA

class HBAView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = StatHBA(csv_name)
        stat_hba_html = stat.resolve()
        context = {'loaded_data': stat_hba_html}
        return render(request, 'stats.html', context)
        # return HttpResponse('esta corriendo')