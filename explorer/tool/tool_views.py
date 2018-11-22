from explorer.models import *
from .tool_serializers import  *
from rest_framework import generics, mixins, viewsets

class ToolList(generics.ListCreateAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializerFull

class ParamList(generics.ListCreateAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParamsSerializer