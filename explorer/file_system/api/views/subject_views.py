from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
import os
import pandas as pd

from django.conf import settings


class SubjectsForDfView(APIView):
    def get(self, params, df):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        meta_loc = pipeline_dir + 'datasets/reads/meta.tsv'

        if os.path.isfile(meta_loc):
            meta = pd.read_csv(meta_loc, sep = '\t')



        subjects = []


        return HttpResponse(subjects, content_type='text/html')
