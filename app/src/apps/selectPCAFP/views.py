from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# from bokeh.embed import components


# import pandas as pd
import os
import glob

class selectPCAFPView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        return render(request, 'selectPCAFP.html')
