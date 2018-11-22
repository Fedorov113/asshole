from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from django.conf import settings
import json
import os


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


# Creates symlinks
class SampleImportView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        src = data['orig_file']
        dst = settings.PIPELINE_DIR+'/datasets/'+data['hdf_name']+'/reads/imp/'+data['sample']+'/'+data['new_name']+'.fastq.gz'

        original_umask = None
        try:
            # stackoverflow.com/questions/5231901/permission-problems-when-creating-a-dir-with-os-makedirs-in-python
            original_umask = os.umask(0)
            if not os.path.isdir(settings.PIPELINE_DIR+'/datasets/'+data['hdf_name']+'/reads/imp/'+data['sample']+'/'):
                os.makedirs(settings.PIPELINE_DIR+'/datasets/'+data['hdf_name']+'/reads/imp/'+data['sample']+'/', 0o777)
            if not os.path.islink(dst):
                os.symlink(src, dst)
        except Exception as Error:
            print(Error)
        finally:
            os.umask(original_umask)

        success = {'success': True}
        if not os.path.islink(dst):
            success['success'] = False

        print(success)

        return HttpResponse(json.dumps(success), content_type='application/json')


