from django.urls import re_path

from .views import DatasetRUDView, DatasetAPIView

urlpatterns = [
    re_path(r'^$', DatasetAPIView.as_view(), name='dataset-create'),
    re_path(r'^(?P<pk>\d+)/$', DatasetRUDView.as_view(), name='dataset-rud'),
]
