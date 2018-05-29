from django.urls import re_path

from .views import PersonRUDView, PersonAPIView


urlpatterns = [
    re_path(r'^person$', PersonAPIView.as_view(), name='persons-list'),
    re_path(r'^person/(?P<pk>\d+)/$', PersonRUDView.as_view(), name='person'),
]