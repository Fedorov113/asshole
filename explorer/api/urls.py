from django.urls import re_path, path
from rest_framework import routers

from explorer.api.views.views import *
from explorer.api.views.sample_views import *
from explorer.api.views.dataset_views import *
# from explorer.api.views.views import CheckSamplesInFolder

router = routers.DefaultRouter()
# router.register(r'sample', SampleFSViewSet, base_name='sample-list')
# router.register(r'ref_seqs', RefSeqSetsView, base_name='ref_seqs-dict')
# router.register(r'sample/mp2', Mp2View.as_view(), base_name='sample-mp2')
urlpatterns = router.urls

# TODO WTF IS GOING ON HERE??

urlpatterns += [
    path('sample/import/', SampleImportView.as_view()),
    path('check_dir/', CheckSamplesInFolder.as_view()),


    re_path(r'^sample/mp2/', Mp2View.as_view()),
    re_path(r'^dataset/$', DatasetsFSView.as_view()),
    re_path(r'^datasets/$', DatasetListView.as_view()),
    re_path(r'^dataset/(?P<df>.+)/preproc', DatasetPreprocsAPIVIew.as_view()),
    re_path(r'^mp2_box/$', Mp2BoxAPIView.as_view()),
    re_path(r'^sample/mp2_scatter/', Mp2ScatterView.as_view()),
    re_path(r'^general_taxa_composition/(?P<df>.+)/(?P<preproc>.+)/(?P<tool>.+)/$', TaxaGeneralCompositionView.as_view()),
    re_path(r'^reads/(?P<df>.+)/(?P<preproc>.+)', ReadsView.as_view()),
    re_path(r'^mapping/(?P<dataset>.+)/(?P<preproc>.+)/(?P<tool>.+)/(?P<seq_type>.+)/(?P<seq_name>.+)/('
            r'?P<postproc>.+)/$', MappedView.as_view()),
]
