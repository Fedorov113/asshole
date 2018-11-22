from django.urls import path

from .views import *

urlpatterns = [
    path('result/', ResultView.as_view()),
    path('result_request/', ResultRequest.as_view()),

    path('profile_result/', ProfileResultList.as_view()),
    path('profile_result/<int:pk>/', ProfileResultDetail.as_view()),
    path('mp2_box/', Mp2BoxAPIView.as_view()),

]
