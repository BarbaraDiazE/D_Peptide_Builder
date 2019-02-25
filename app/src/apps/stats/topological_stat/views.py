from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

import pandas as pd
import os
import glob

from .compute_topological import statTOPOLOGICAL

class TOPOLOGICALView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = statTOPOLOGICAL(csv_name)
        stat_topological_html = stat.resolve()
        context = {'loaded_data': stat_topological_html}
        return render(request, 'stats_topological.html', context)