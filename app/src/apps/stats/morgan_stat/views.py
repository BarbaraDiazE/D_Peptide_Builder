from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

import pandas as pd
import os
import glob

from .compute import statMORGAN

class MORGANView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        stat = statMORGAN(csv_name)
        stat_morgan_html = stat.resolve()
        context = {'loaded_data': stat_morgan_html}
        return render(request, 'stats_morgan.html', context)