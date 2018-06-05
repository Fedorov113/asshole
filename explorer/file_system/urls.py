from django.urls import re_path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SampleFSViewSet
from .views import Mp2View
from .views import RefSeqSetsView

router = routers.DefaultRouter()
router.register(r'sample', SampleFSViewSet, base_name='sample-list')
router.register(r'ref_seqs', RefSeqSetsView, base_name='ref_seqs-dict')
# router.register(r'sample/mp2', Mp2View.as_view(), base_name='sample-mp2')
urlpatterns = router.urls


urlpatterns += [
    re_path(r'^sample/mp2', Mp2View.as_view())
]