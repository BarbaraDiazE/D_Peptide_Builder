from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

from .compute_Morgan3 import GenerateMorgan


# Create your views here.
class Morgan3View(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        gm = GenerateMorgan(csv_name)
        plot = gm.resolve()
        script, div = components(plot)
        return render_to_response('plot_morgan.html', {'script': script, 'div': div})