from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.embed import components

from rest_framework.views import APIView

from .compute_topological import GenerateTopological


# Create your views here.
class TopologicalView(APIView):

    def get(self, request):
        csv_name = request.session['csv_name']
        gm = GenerateTopological(csv_name)
        plot = gm.resolve()
        script, div = components(plot)
        return render_to_response('plot_topological.html', {'script': script, 'div': div})
         # return HttpResponse('holi')