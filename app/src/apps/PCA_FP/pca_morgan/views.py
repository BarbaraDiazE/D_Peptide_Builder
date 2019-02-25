from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

import pandas as pd
import os
import glob

from .compute_pca_fp import GeneratePCA


class PCAMORGANView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']  
        pca = GeneratePCA(csv_name)
        plot = pca.resolve()
        script, div = components(plot)
        return render_to_response('plot_PCAFP.html', {'script': script, 'div': div})
