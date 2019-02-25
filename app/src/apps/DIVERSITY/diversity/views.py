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

class diversityView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        return render(request, 'diversity.html')
