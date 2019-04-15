from explorer.celery_snake import generate_files_for_snake_from_request_dict
from explorer.models import *
from explorer.tasks import *

from django.http import HttpResponse
from rest_framework.views import APIView
import json

from celery import uuid
from rest_framework import status
from rest_framework.response import Response


class CelerySnakemakeFromJSON(APIView):
    def post(self, request):
        res_req = json.loads(request.body)
        task_id = uuid()
        res_locs = generate_files_for_snake_from_request_dict(res_req)
        print(res_locs)
        if isinstance(res_locs, (list,)):
            print('its a list')
            if len(res_locs) > 0:
                print(' run snake')
                snakemake_run \
                    .apply_async((res_locs, res_req.get('dry', 0),
                                  res_req['threads'], res_req['jobs']), task_id=task_id)
                return Response('Requested ' + str(len(res_locs)) + ' results',
                                status=status.HTTP_202_ACCEPTED,
                                content_type='application/json')
            else:
                return Response('Nothing to be done',
                                status=status.HTTP_200_OK,
                                content_type='application/json')
        else:
            return Response('Something went wrong',
                            status=status.HTTP_400_BAD_REQUEST)


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

        return HttpResponse(json.dumps({'start': 'SUCCESS'}), content_type='application/json')
