from django.urls import re_path
from rest_framework import routers

from explorer.file_system.api.views import *

router = routers.DefaultRouter()
router.register(r'sample', SampleFSViewSet, base_name='sample-list')
router.register(r'ref_seqs', RefSeqSetsView, base_name='ref_seqs-dict')
# router.register(r'sample/mp2', Mp2View.as_view(), base_name='sample-mp2')
urlpatterns = router.urls

urlpatterns += [
    re_path(r'^sample/mp2/', Mp2View.as_view()),
    re_path(r'^dataset/$', DatasetsFSView.as_view()),
    re_path(r'^dataset/(?P<df>.+)/preproc', DatasetPreprocsAPIVIew.as_view()),
    re_path(r'^mp2_box/$', Mp2BoxAPIView.as_view()),
    re_path(r'^sample/mp2_scatter/', Mp2ScatterView.as_view()),
    re_path(r'^reads/(?P<df>.+)/(?P<preproc>.+)', ReadsView.as_view()),
    re_path(r'^mapping/(?P<dataset>.+)/(?P<preproc>.+)/(?P<tool>.+)/(?P<seq_type>.+)/(?P<seq_name>.+)/(?P<postproc>.+)/$',MappedView.as_view())
]
