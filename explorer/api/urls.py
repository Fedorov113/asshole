from django.urls import re_path, path
from rest_framework import routers

from explorer.api.views.views import *
from explorer.api.views.sample_views import *
from explorer.api.views.dataset_views import *
from explorer.api.views.source_views import *
from explorer.api.views.biospecimen_views import *
# from explorer.api.views.views import CheckSamplesInFolder

router = routers.DefaultRouter()
urlpatterns = router.urls

# TODO WTF IS GOING ON HERE??

urlpatterns += [
    path('dataset/', DatasetListView.as_view()),
    path('dataset/<str:df>/', SamplesForDfFs.as_view()),
    path('dataset/<str:df>/source/', SourcesForDfFs.as_view()),
    path('dataset/<str:df>/biospecimen/', BiospecimensForDfFs.as_view()),

    path('sample/import/', SampleImportView.as_view()),
    path('check_dir/', CheckSamplesInFolder.as_view()),


    path('_dataset/<str:df>/', DatasetFullView.as_view()),
    path('dataset/<str:df>/preproc', DatasetPreprocsAPIVIew.as_view()),
    path('reads/<str:df>/<str:preproc>', ReadsView.as_view()),

    # re_path(r'^sample/mp2/', Mp2View.as_view()),
    # re_path(r'^dataset/$', DatasetsFSView.as_view()),
    #
    # re_path(r'^mp2_box/$', Mp2BoxAPIView.as_view()),
    # re_path(r'^sample/mp2_scatter/', Mp2ScatterView.as_view()),
    # re_path(r'^general_taxa_composition/(?P<df>.+)/(?P<preproc>.+)/(?P<tool>.+)/$', TaxaGeneralCompositionView.as_view()),
    # re_path(r'^mapping/(?P<dataset>.+)/(?P<preproc>.+)/(?P<tool>.+)/(?P<seq_type>.+)/(?P<seq_name>.+)/('
    #         r'?P<postproc>.+)/$', MappedView.as_view()),
]
