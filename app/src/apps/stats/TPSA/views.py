from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

import pandas as pd
import os
import glob

from .compute_TPSA import StatTPSA

class TPSAView(APIView):
   
    def get(self, request):
        csv_name = request.session['csv_name']
        stat = StatTPSA(csv_name)
        stat_tpsa_html = stat.resolve()
        context = {'loaded_data': stat_tpsa_html}
        return render(request, 'stats.html', context)