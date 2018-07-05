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
        # What information do we want to include in each df?
        # This object can be constructed only if there is at least one sample in reads/raw folder
        # {
        #     df_name: df_name,
        #     description: description from df_name.info file, if present,
        #     num_samples: number of samples in reads/raw folder
        # }
        for dataset in datasets:
            if os.path.isdir(dataset):
                datasets_list.append(dataset.replace(pipeline_dir + 'datasets/', ''))


        return HttpResponse(json.dumps(datasets_list), content_type='application/json')
