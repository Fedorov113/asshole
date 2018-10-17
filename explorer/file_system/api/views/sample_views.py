from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from django.conf import settings
import json


class SampleFastQCView(APIView):
    def get(self, params, df, preproc, sample, strand):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{df}/reads/{preproc}/{sample}/{sample}_{strand}_fastqc.html'
        search_dir = search_dir.format(df=df, preproc=preproc, sample=sample, strand=strand)

        fastqc_html = ''
        with open(search_dir, 'r') as fastqc_file:
            fastqc_html = fastqc_file.read()

        return HttpResponse(fastqc_html, content_type='text/html')

class SampleKronaView(APIView):
    def get(self, params, df, preproc, sample, tool):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{df}/taxa/reads/{preproc}/{tool}/{sample}/krona.html'
        search_dir = search_dir.format(df=df, preproc=preproc, sample=sample, tool=tool)

        krona_html = ''
        with open(search_dir, 'r') as krona_html_file:
            krona_html = krona_html_file.read()

        return HttpResponse(krona_html, content_type='text/html')

class SampleImportView(APIView):
    def post(self, request):
        print(request.data )
        return HttpResponse(json.dumps(request.data), content_type='application/json')


