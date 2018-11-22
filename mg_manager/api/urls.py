from django.urls import path, include

from .views import *

urlpatterns = [
    path('dataset_hard/', DatasetHardList.as_view(), name='dataset-hard-list'),
    path('dataset_hard_full/', DatasetHardFull.as_view(), name='dataset-hard-full'),
    path('dataset_hard/<int:pk>/', DatasetHardDetail.as_view(), name='dataset-rud'),

    path('dataset_hard/<int:pk>/mg_sample/', MgSampleList.as_view(), name='mg-sample-list-dataset'),

    path('dataset_hard/<int:pk>/source/', SampleSourceList.as_view()),
    path('dataset_hard/<int:hdf_pk>/mg_sample/<int:pk>', MgSampleDetail.as_view(),
         name='mg-sample-hdf-detail'),
    path('mg_sample/<int:pk>', MgSampleDetail.as_view(), name='mg-sample-detail'),
    path('sample_source/', SampleSourceList.as_view()),
    # path('dataset_hard/<int:hdf_pk>/mg_sample/<int:pk>/file_container', MgSampleFileContainerList.as_view()),

    path('library/', LibraryList.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetail.as_view(), name='library-rud'),

    path('mg_sample/', MgSampleList.as_view(), name='mg-sample-list'),
    path('real_sample/', RealSampleAPIView.as_view(), name='real-sample-list'),
    path('', include(('mg_manager.result.urls', 'result'), namespace='mgms'))
]
