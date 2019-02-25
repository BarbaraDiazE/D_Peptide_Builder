from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

from .compute_atom import GenerateAtom

# Create your views here.
class AtomView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        gf = GenerateAtom(csv_name)
        plot = gf.resolve()
        script, div = components(plot)
        return render_to_response('plot_atom.html', {'script': script, 'div': div})