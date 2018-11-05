from django.urls import path, include
from . import views

from .tool.tool_views import *
from .result.views import *

urlpatterns = [
    # path('test_celery/', views.TestCelery.as_view()),
    path('celery_snakemake_list/', views.CelerySnakemakeFromList.as_view()),

    path('seq_set/', views.sequence_explorer),
    path('seq_set/<category>/<seq_set_name>', views.sequence_set),
    path('tool/', ToolList.as_view()),

    path('result_types/', ResultTypeList.as_view()),
    path('results/', ResultList.as_view()),
    path('schema/<schema_object>', SchemaView.as_view())
]
