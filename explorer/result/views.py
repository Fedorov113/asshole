import json
import requests
import jsonref
import glob

from django.http import HttpResponse
from rest_framework.views import APIView

from explorer.RuleSerializer import RuleSerializer
from .serializers import *
from rest_framework import generics


class ResultTypeList(generics.ListCreateAPIView):
    queryset = ResultType.objects.all()
    serializer_class = ResultTypeSerializer


class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class SchemaView(APIView):
    def get(self, request, schema_object):
        schema = Schema.objects.get(schema_name=schema_object)
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


class ResultView(APIView):
    def get(self, request):
        with open('/data6/bio/TFM/pipeline/results/quality/count.json') as schema_file:
            schema = jsonref.loads(schema_file.read(), base_uri='file:///data6/bio/TFM/pipeline/', jsonschema=True)

        rr = repr(schema)
        print(type(rr))
        rr = rr.replace("'", '"')
        rr = rr.replace("None", 'null')
        print(rr)

        rrr = json.loads(rr)
        return HttpResponse(json.dumps(rrr), content_type='application/json')


class ResultTypeListFS(APIView):
    def get(self, request):
        loc = os.path.join(settings.PIPELINE_DIR, 'results/*')
        result_types = glob.glob(loc)

        data = []

        for res in result_types:
            if os.path.isfile(res+'/info'):
                with open(res+'/info') as f:
                    data.append(json.load(f))

        return HttpResponse(json.dumps(data), content_type='application/json')

class ResultListFS(APIView):
    def get(self, request):
        loc = os.path.join(settings.PIPELINE_DIR, 'results/*/*.json')
        # results = [f.split('/')[-1].split('.')[0] for f in glob.glob(loc)]
        results = glob.glob(loc)
        to_send = []
        for res in results:
            with open(res) as schema_file:
                schema = jsonref.loads(schema_file.read(), base_uri='file:///data6/bio/TFM/pipeline/', jsonschema=True)

            rr = repr(schema)
            rr = rr.replace("'", '"')
            rr = rr.replace("None", 'null')
            to_send.append(json.loads(rr))

        return HttpResponse(json.dumps(to_send), content_type='application/json')
