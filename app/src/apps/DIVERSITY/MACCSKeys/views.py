from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

from .compute import GenerateFingerprint


# Create your views here.
class MACCKeysView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        gf = GenerateFingerprint(csv_name)
        plot = gf.resolve()
        script, div = components(plot)
        return render_to_response('plot_maccskeys.html', {'script': script, 'div': div})