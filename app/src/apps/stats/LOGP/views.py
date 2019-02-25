from rest_framework.views import APIView
from django.http import HttpResponse

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

import pandas as pd
import os
import glob

from .compute_LOGP import StatLOGP

class LOGPView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = StatLOGP(csv_name)
        stat_logp_html = stat.resolve()
        context = {'loaded_data': stat_logp_html}
        return render(request, 'stats.html', context)        