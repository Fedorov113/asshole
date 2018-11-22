from explorer.models import *
from explorer.tasks import *

from django.http import HttpResponse
from rest_framework.views import APIView
import json

from celery import uuid

# from Bio import SeqIO



class CelerySnakemakeFromJSON(APIView):
    def post(self, request):
        task_id = uuid()
        data = json.loads(request.body)
        print(data)
        desired = data['desired_results']

        # create out_loc from JSON
        res = Result.objects.get(result_name=desired['result'])
        print(res.json_in_to_loc_out_func)

        input_loc_list = []
        if res.json_in_to_loc_out_func == 'simple':
            out_wc = res.out_str_wc
            input_objects = desired['input_objects']

            for input in desired['input']:
                input_loc_list.append(out_wc.format(**input[input_objects[0]]))

        print(input_loc_list)

        snakemake_run.apply_async((input_loc_list, 0, desired['threads'], desired['jobs']), task_id=task_id)


        return HttpResponse (json.dumps({'got': 'it'}), content_type='application/json')



class CelerySnakemakeFromList(APIView):
    def post(self, request):
        task_id = uuid()
        data = json.loads(request.body)
        desired_files = data['desired_files']
        dry = int(request.GET.get('dry', 1))
        drmaa = int(request.GET.get('drmaa', 0))
        jobs = int(request.GET.get('jobs', 1))
        threads = int(request.GET.get('threads', 1))

        # Run snakemake
        snakemake_run.apply_async((desired_files, dry, threads, jobs), task_id=task_id)

        return HttpResponse (json.dumps({'start': 'SUCCESS'}), content_type='application/json')





