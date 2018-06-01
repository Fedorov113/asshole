from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^dataset$', DatasetAPIView.as_view(), name='dataset-create'),
    re_path(r'^dataset/(?P<pk>\d+)/$', DatasetRUDView.as_view(), name='dataset-rud'),
    re_path(r'^subject/$', SubjectAPIView.as_view(), name='subject-list-create'),
    re_path(r'^subject/(?P<pk>\d+)/$', SubjectRUDView.as_view(), name='subject-rud'),
    re_path(r'^actual_shit/$', ActualShitAPIView.as_view(), name='actual_shit-list-create'),

]
