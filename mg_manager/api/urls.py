from django.urls import path, include

from .views import *

urlpatterns = [
    path('real_sample/', RealSampleList.as_view()),
    path('source/', SampleSourceList.as_view()),

    path('dataset_hard/', DatasetHardList.as_view(), name='dataset-hard-list'),
    path('mg_sample/', MgSampleList.as_view(), name='mg-sample-list'),
    path('mg_sample_container/', MgSampleContainerList.as_view(), name='mg-sample-container-list'),
    path('mg_sample_container_file/', MgSampleContainerFileList.as_view(), name='mg-sample-container-file-list'),

    path('mg_sample_lookup/', MgSampleNewList.as_view(), name='mg-sample-lookup'),

    path('dataset_hard_full/', DatasetHardFull.as_view(), name='dataset-hard-full'),
    path('dataset_hard/<int:pk>/', DatasetHardDetail.as_view(), name='dataset-rud'),

    path('dataset_hard/<int:pk>/mg_sample/', MgSampleFullList.as_view(), name='mg-sample-list-dataset'),
    # path('dataset_hard/<int:pk>/mg_new/', MgSampleNewList.as_view()),
    path('dataset_hard/<int:pk>/mg_other/', MgSampleOther.as_view()),




    path('dataset_hard/<int:hdf_pk>/mg_sample/<int:pk>', MgSampleDetail.as_view(),
         name='mg-sample-hdf-detail'),
    path('mg_sample/<int:pk>', MgSampleDetail.as_view(), name='mg-sample-detail'),

    path('sample_source/', SampleSourceList.as_view()),

    path('library/', LibraryList.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetail.as_view(), name='library-rud'),

    path('mg_sample_full/', MgSampleFullList.as_view(), name='mg-sample-list'),
    # path('real_sample/', RealSampleAPIView.as_view(), name='real-sample-list'),
    path('', include(('mg_manager.result.urls', 'result'), namespace='mgms')),

    path('sequencing_run/', SequencingRunList.as_view(), name='SequencingRunList-list'),
    # path('<int:pk>/test/', Test.as_view()),

]
