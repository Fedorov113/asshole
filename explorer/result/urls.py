from django.urls import path

from .views import ResultView

urlpatterns = [
    path('real_sample/', ResultView.as_view()),
]
