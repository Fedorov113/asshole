from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from .serializers import *
from django.db.models import Q


class FsContainerList(APIView):
    def get(self, request):
        samples = []
        hdf = request.query_params.get('hdf', None)
        run = request.query_params.get('run', None)
        source = request.query_params.get('source', None)
        preproc = request.query_params.get('preproc', None)

        query = {}
        if hdf is not None:
            query['dataset_hard'] = hdf
        if run is not None:
            query['sequencing_run'] = run
        if source is not None:
            query['source'] = source

        # df = DatasetHard.objects.get(pk=hdf).df_name
        mg_samples = MgSample.objects.filter(**query).prefetch_related('containers').select_related('dataset_hard')

        for sample in mg_samples:
            preproc = ''
            for container in sample.containers.all():
                if len(container.preprocessing) > len(preproc):
                    preproc = container.preprocessing
            df = sample.dataset_hard.df_name
            samples.append(
                {'id': sample.id,
                 'name': sample.name,
                 'name_on_fs': sample.name_on_fs,
                 "df": df,
                 "preproc": preproc,
                 "real_sample": sample.real_sample_id,
                 "source": sample.source_id,
                 "library": sample.library_id,
                 "sequencing_run": sample.sequencing_run_id}
            )

        return HttpResponse(json.dumps(samples), content_type='application/json')
