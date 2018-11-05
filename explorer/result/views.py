from django.http import HttpResponse
from rest_framework.views import APIView

from explorer.models import *
from .serializers import  *
from rest_framework import generics, mixins, viewsets

class ResultTypeList(generics.ListCreateAPIView):
    queryset = ResultTypes.objects.all()
    serializer_class = ResultTypeSerializer

class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class SchemaView(APIView):
    def get(self, request, schema_object):
        schema = Schema.objects.get(schema_name=schema_object)
        # schema = '{"type":"object","title":"MgSampleFileContainer","required":["df","preproc","sample"],"properties":{"df":{"type":"string","title":"Dataset","default":""},"sample":{"type":"string","title":"Sample name (on fs?)","default":"","shit":"is tasty"},"preproc":{"type":"string","title":"Preprocessing","default":""}}}'
        return HttpResponse(schema.schema, content_type='application/json')
