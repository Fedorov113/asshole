from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views
urlpatterns = [
    re_path('.*', views.index ),
    # path(r'^.*/', TemplateView.as_view(template_name="index.html"), name='index')
]