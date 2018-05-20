from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /explorer/2/
    path('<int:df_id>/', views.dataset, name='dataset'),
    path('<int:df_id>/sample/<sample_name>/how/<how>/<strand>/fastqc', views.fastqc),
    path('<int:df_id>/sample/<sample_name>/', views.sample),
    path('seq_set/', views.sequence_explorer),
    path('seq_set/<category>/<seq_set_name>', views.sequence_set),
]