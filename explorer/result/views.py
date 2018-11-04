from explorer.models import *
from .serializers import  *
from rest_framework import generics, mixins, viewsets

class ResultTypeList(generics.ListCreateAPIView):
    queryset = ResultTypes.objects.all()
    serializer_class = ResultTypeSerializer

class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer