from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

import pandas as pd
import os
import glob

from .compute_MW import StatMW

class MWView(APIView):
      
    def get(self, request):
        csv_name = request.session['csv_name']
        stat = StatMW(csv_name)
        stat_mw_html = stat.resolve()
        context = {'loaded_data': stat_mw_html}
        return render(request, 'stats.html', context) 