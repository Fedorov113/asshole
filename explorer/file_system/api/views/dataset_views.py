from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
import glob
import os
import json

from django.conf import settings


class DatasetListView(APIView):
    def get(self, request):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        search_dir = pipeline_dir + 'datasets/*'
        datasets = glob.glob(search_dir)

        datasets_list = []
        for dataset in datasets:
            if os.path.isdir(dataset):
                datasets_list.append(dataset.replace(pipeline_dir + 'datasets/', ''))

        # What information we want to include in each sample?
        # {
        #     df_name: df_name,
        #     description: description from df_name.info file,
        #     num_samples: number of samples in reads/raw folder
        # }
        return HttpResponse(json.dumps(datasets_list), content_type='application/json')
