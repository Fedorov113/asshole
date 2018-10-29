from django.urls import path, include
from . import views

urlpatterns = [
    # path('test_celery/', views.TestCelery.as_view()),
    path('celery_snakemake_list/', views.CelerySnakemakeFromList.as_view()),

    path('seq_set/', views.sequence_explorer),
    path('seq_set/<category>/<seq_set_name>', views.sequence_set),
]
