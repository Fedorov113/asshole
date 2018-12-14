import json
import requests

from django.http import HttpResponse
from rest_framework.views import APIView

from asshole import settings
from explorer.RuleSerializer import RuleSerializer
from explorer.models import *
from .serializers import *
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


class RuleResultView(APIView):
    """

    """

    def get(self, request, rule_result_id):
        snrr = SnakeRuleResult.objects.get(pk=rule_result_id)

        ser = RuleSerializer(snrr.rule_name, snrr.output_to_serialize)
        dd = ser.get_dict()

        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        url = settings.ASSHOLE_URL + 'api/mgms/result/'
        r = requests.post(url, data=json.dumps(dd), headers=headers)
        return HttpResponse(json.dumps(str(r)), content_type='application/json')
