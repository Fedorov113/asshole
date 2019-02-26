from django.urls import path, include
from . import views

from .tool.tool_views import *
from .result.views import *

urlpatterns = [
    # path('test_celery/', views.TestCelery.as_view()),
    path('celery_snakemake_list/', views.CelerySnakemakeFromList.as_view()),
    path('request_result/', views.CelerySnakemakeFromJSON.as_view()),

    path('tool/', ToolList.as_view()),
    path('param/', ParamList.as_view()),

    path('result_types/', ResultTypeList.as_view()),
    path('results/', ResultList.as_view()),
    path('schema/<schema_object>', SchemaView.as_view()),
    path('rule_result/<int:rule_result_id>/', RuleResultView.as_view()),

    path('result_test/', ResultView.as_view()),
    path('result_types_fs/', ResultTypeListFS.as_view()),
    path('results_fs/', ResultListFS.as_view()),

]
