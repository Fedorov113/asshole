from explorer.tasks import *
from django.conf import settings
import os, glob

from django.http import HttpResponse
from rest_framework.views import APIView
import json

from celery import uuid

from django.shortcuts import render
# from Bio import SeqIO

def get_fastqc(df_name, batch_name, how, sample_name, strand):
    fastqc_html = ''
    fastqc_html_loc = os.path.join(settings.PIPELINE_DIR, 'datasets/'\
                      + df_name +'/reports/fastqc/'+sample_name+'/'+how+'/' +strand+'_fastqc.html')

    with open(fastqc_html_loc, 'r') as content_file:
        fastqc_html = content_file.read()


    return fastqc_html



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)



def get_folders_in_path(directory):
    return [d for d in os.listdir(directory)
            if (os.path.isdir(os.path.join(directory, d))) and
            d[0] != '.']


def get_files_from_path_with_ext(directory, extension, only_names = True):
    return [
        item.split("/")[-1].split(extension)[0]
        for item in glob.glob(directory  + '*' + extension)
    ]


def sequence_explorer(request):
    categories_and_fasta ={}
    # Get categories
    ref_sequences_dir = os.path.join(settings.PIPELINE_DIR, 'data/ref/')
    categories = get_folders_in_path(ref_sequences_dir)
    categories.remove('index')

    # Get fasta files from each category
    for category in categories:
        cat_fasta_dir = os.path.join(settings.PIPELINE_DIR, 'data/ref/'+category+'/')
        categories_and_fasta[category] = get_files_from_path_with_ext(cat_fasta_dir, '.fa')

    context = {
        'categories': categories_and_fasta
    }
    return render(request, 'explorer/sequence_explorer.html', context)

def get_sequences_info_from_fasta(category, fasta_name, ext):
    ref_sequences_dir = os.path.join(settings.PIPELINE_DIR, 'data/ref/'+category+'/'+fasta_name+ext)
    return None #SeqIO.to_dict(SeqIO.parse(ref_sequences_dir, "fasta"))

def sequence_set(request, category, seq_set_name):
    context = {
        'category': category,
        'seq_set_name': seq_set_name,
        'sequences': get_sequences_info_from_fasta(category, seq_set_name, '.fa').keys()
    }
    return render(request, 'explorer/sequence_set.html', context)

# class DatasetViewSet(generics.ListCreateAPIView):
#     """
#     API endpoint that allows datasets to be viewed or edited.
#     """
#     queryset = Dataset.objects.all()
#     serializer_class = DatasetSerializer






class TestCelery(APIView):
    def post(self, request):
        data = json.loads(request.body)
        samples_list = data['samples_list']
        print(samples_list)
        return HttpResponse (json.dumps('Well, weve started mult'), content_type='application/json')


class TestCelerySnakemake(APIView):
    def post(self, request):

        data = json.loads(request.body)
        samples_list = data['samples_list']

        snakemake_run.delay(samples_list)

        return HttpResponse (json.dumps("Well, we've started snakemake. Let's how it ends."), content_type='application/json')



class CelerySnakemakeFromList(APIView):
    def post(self, request):
        task_id = uuid()
        data = json.loads(request.body)
        samples_list = data['samples_list']

        # sn_loc = generate_snakefile(samples_list, task_id)

        dry = int(request.GET.get('dry', 1))

        print(task_id)
        # Run snakemake by file identificator
        snakemake_run.apply_async((samples_list, dry), task_id=task_id)

        return HttpResponse (json.dumps("Well, we've started snakemake"), content_type='application/json')  





