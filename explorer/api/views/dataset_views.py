from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
import glob
import os
import json

from django.conf import settings
from explorer.file_system.file_system_helpers import *

import pandas as pd

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

class TaxaGeneralCompositionView(APIView):
    def get(self, request, df, preproc, tool):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{df}/taxa/reads/{preproc}/{tool}/*/krak.tsv'
        search_dir_w_sample = datasets_dir + '{df}/taxa/reads/{preproc}/{tool}/{sample}/krak.tsv'

        search_dir = search_dir.format(df=df, preproc=preproc, tool=tool)
        search_dir_w_sample = search_dir.replace('*', '{sample}')

        meta_loc = datasets_dir+df+'/reads/meta.tsv'
        general_compositions = []

        if os.path.isfile(meta_loc):
            meta = pd.read_csv(meta_loc, sep='\t')
            samples = meta['sample']
            for s in samples:
                file_loc = search_dir_w_sample.format(sample=s)
                comp = get_general_taxa_comp_for_sample(file_loc)
                if comp is not None:
                    general_compositions.append(comp)
        else:
            reports = glob.glob(search_dir)
            for report in reports:
                general_compositions.append(get_general_taxa_comp_for_sample(report))

        return HttpResponse(json.dumps(general_compositions), content_type='application/json')

