"""Peptide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from django.contrib import admin
from django.conf import settings
# from apps.Build.views import ServerViews
from apps.Build.views import ServerViews, CSVView, DownloadCSV
from apps.PCA.views import PCAView
from apps.PCA_FP.pca_topological.views import PCAFPView
from apps.PCA_FP.pca_morgan.views import PCAMORGANView
from apps.PCA_FP.pca_morgan3.views import PCAMORGAN3View
from apps.PCA_FP.pca_maccs.views import PCAMACCSView
from apps.PCA_FP.pca_atom.views import PCAATOMView
from apps.perplexity.views import PerplexityViews
from apps.TSNE.TSNE_Topological.views import TSNEtopologicoView
# from apps.T-SNE.TSNE_M2 import TSNEmorgan2View
from apps.TSNE.TSNE_Morgan.views import TSNEmorganView
from apps.TSNE.TSNE_Morgan3.views import TSNEmorgan3View
from apps.TSNE.TSNE_Maccs.views import TSNEmaccsView
from apps.TSNE.TSNE_Atom.views import TSNEatomView
from apps.DIVERSITY.MACCSKeys.views import MACCKeysView
from apps.DIVERSITY.Morgan.views import MorganView
from apps.DIVERSITY.Morgan3.views import Morgan3View
from apps.DIVERSITY.Atom.views import AtomView
from apps.DIVERSITY.Topological.views import TopologicalView
from apps.stats.HBA.views import HBAView
from apps.stats.HBD.views import HBDView
from apps.stats.RB.views import RBView
from apps.stats.TPSA.views import TPSAView
from apps.stats.LOGP.views import LOGPView
from apps.stats.MW.views import MWView
from apps.stats.maccs_stat.views import MACCSView
from apps.stats.morgan_stat.views import MORGANView
from apps.stats.atom_stat.views import ATOMView
from apps.stats.topological_stat.views import TOPOLOGICALView
from apps.DIVERSITY.diversity.views import diversityView
from apps.selectTSNE.views import selectTSNEView
from apps.selectPCAFP.views import selectPCAFPView
# from apps.stats.topological_stat import  TOPOLOGICALView

urlpatterns = [
    # url(r'^$', ServerViews.index),
    url(r'^$', ServerViews.as_view()),
    url(r'^csv$', CSVView.as_view(), name='render-csv'),
    url(r'^csv/(?P<csv_name>.+)/$', CSVView.as_view()),
    url(r'^download_csv$', DownloadCSV.as_view()),
    # url(r'^download_csv/(?P<csv_name>.+)/$', DownloadCSV.as_view(), name='download_csv'),
    url(r'^pca$', PCAView.as_view()),
    url(r'^pcafp$', PCAFPView.as_view()),
    url(r'^pcamorgan$', PCAMORGANView.as_view()),
    url(r'^pcamorgan3$', PCAMORGAN3View.as_view()),
    url(r'^pcaatom$', PCAATOMView.as_view()),
    url(r'^pcamaccs$', PCAMACCSView.as_view()),
    # url(r'^perplexity$', PerplexityViews.as_view()),
    url(r'^TSNEtopologico$', TSNEtopologicoView.as_view()),
    url(r'^TSNEmorgan$', TSNEmorganView.as_view()),
    url(r'^TSNEmorgan3$', TSNEmorgan3View.as_view()),
    url(r'^TSNEmaccs$', TSNEmaccsView.as_view()),
    url(r'^TSNEatom$', TSNEatomView.as_view()),
    url(r'^maccskeys$', MACCKeysView.as_view()),
    url(r'^morgan$', MorganView.as_view()),
    url(r'^morgan3$', Morgan3View.as_view()),
    url(r'^atom$', AtomView.as_view()),
    url(r'^topological$', TopologicalView.as_view()),
    url(r'^HBA$', HBAView.as_view()),
    url(r'^HBD$', HBDView.as_view()),
    url(r'^RB$', RBView.as_view()),
    url(r'^TPSA$', TPSAView.as_view()),
    url(r'^LogP$', LOGPView.as_view()),
    url(r'^MW$', MWView.as_view()),
    url(r'^maccs_stat$', MACCSView.as_view()),
    url(r'^morgan_stat$', MORGANView.as_view()),
    url(r'^atom_stat$', ATOMView.as_view()),
    url(r'^topological_stat$', TOPOLOGICALView.as_view()),
    url(r'^diversity$', diversityView.as_view()),
    url(r'^selectTSNE$', selectTSNEView.as_view()),
    url(r'^selectPCAFP$', selectPCAFPView.as_view()),
]