from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from django.conf import settings


class SampleFastQCView(APIView):
    def get(self, params, df, preproc, sample, strand):
        # HARDCODED FOR DEV PURPOSE
        # TODO make fetching fastqc report normal

        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{df}/reads/{preproc}/{sample}/{sample}_{strand}_fastqc.html'
        search_dir = search_dir.format(df=df, preproc=preproc, sample=sample, strand=strand)

        fastqc_html = ''
        with open(search_dir, 'r') as fastqc_file:
            fastqc_html = fastqc_file.read()

        return HttpResponse(fastqc_html, content_type='text/html')