from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os, glob
from .models import Dataset
from django.template import loader
from django.http import Http404
from django.shortcuts import render
from Bio import SeqIO

from explorer.serializers import DatasetSerializer
from rest_framework import generics

# Create your views here.

# Show datasets
def index(request):
    return HttpResponse("Hello, world. This is an entry point to asshole.")

# Dataset main view



def get_fastqc(df_name, batch_name, how, sample_name, strand):
    fastqc_html = ''
    fastqc_html_loc = os.path.join(settings.PIPELINE_DIR, 'datasets/'\
                      + df_name +'/reports/fastqc/'+sample_name+'/'+how+'/' +strand+'_fastqc.html')

    with open(fastqc_html_loc, 'r') as content_file:
        fastqc_html = content_file.read()


    return fastqc_html

def dataset(request, df_id):
    try:
        df_name=Dataset.objects.get(pk = df_id).df_name
    except Dataset.DoesNotExist:
        raise Http404("NO SUCH DATASET")

    context = {
        'df_name': df_name,
        'files': get_samples_for_df(df_name, 0)
    }

    return render(request, 'explorer/index.html', context)

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def sample(request, df_id,sample_name):
    try:
        df_name=Dataset.objects.get(pk = df_id).df_name
    except Dataset.DoesNotExist:
        raise Http404("NO SUCH DATASET")

    # Check all reads files that exist for this sample
    reads_dir = os.path.join(settings.PIPELINE_DIR, 'datasets/'
                                     + df_name
                                     + '/reads/')
    dirs_with_reads = get_folders_in_path(reads_dir)

    fastqgz_files_dir = reads_dir + '%s/'
    fff = {}
    for dir in dirs_with_reads:
        directory = fastqgz_files_dir % dir
        if len(glob.glob(directory+sample_name+'*.fastq.gz')) > 0:
            reads_files = get_files_from_path_with_ext(directory+sample_name, '.fastq.gz')
            reads_files.sort()
            # os.stat('C:\\Python27\\Lib\\genericpath.py').st_size
            reads_files_info = []
            for file in reads_files:
                f_size = os.stat(directory+file+'.fastq.gz').st_size
                reads_files_info.append([file, sizeof_fmt(f_size)])
            print(reads_files_info)
            fff[dir] = reads_files_info

    context = {
        'files': fff,
        'sample_name': sample_name
    }
    return render(request, 'explorer/sample.html', context)

def fastqc(request, df_id, sample_name, strand, how):
    try:
        df_name=Dataset.objects.get(pk = df_id).df_name
    except Dataset.DoesNotExist:
        raise Http404("NO SUCH DATASET")

    try:
        fastqc = get_fastqc(df_name, 0, how, sample_name, strand)
    except Exception:
        raise Http404('NO FASTQC REPORT FOR ' + sample_name)
    context = {
        'fastqc': fastqc
    }
    return render(request, 'explorer/fastqc.html', context)

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
    return SeqIO.to_dict(SeqIO.parse(ref_sequences_dir, "fasta"))

def sequence_set(request, category, seq_set_name):
    context = {
        'category': category,
        'seq_set_name': seq_set_name,
        'sequences': get_sequences_info_from_fasta(category, seq_set_name, '.fa').keys()
    }
    return render(request, 'explorer/sequence_set.html', context)

class DatasetViewSet(generics.ListCreateAPIView):
    """
    API endpoint that allows datasets to be viewed or edited.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
