from django.urls import re_path

from .views import DatasetRUDView, DatasetAPIView

urlpatterns = [
    re_path(r'^dataset$', DatasetAPIView.as_view(), name='dataset-create'),
    re_path(r'^dataset/(?P<pk>\d+)/$', DatasetRUDView.as_view(), name='dataset-rud'),
]
