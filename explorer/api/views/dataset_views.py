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

import sys

sys.path.insert(0, '/data6/bio/TFM/pipeline/anal/fedorov/notebooks/dev_ass/')
import loaders as assload


class DatasetListView(APIView):
    def get(self, request):
        print('getting datasets')
        return HttpResponse(json.dumps(assload.load_dfs_from_db(settings.ASSNAKE_DB)), content_type='application/json')


class SchemasInDf(APIView):
    def get(self, request, df):
        schemas = [s.split('/')[-1].replace('schema_source__', '').replace('.json', '') for s in
         glob.glob('/data5/bio/databases/assnake/datasets/{df}/schema_source__*.json'.format(df=df))]
        return HttpResponse(json.dumps(schemas), content_type='application/json')

class SamplesForDfFs(APIView):
    def get(self, request, df):
        mg_samples = assload.load_mg_samples_in_df(df, settings.ASSNAKE_DB, 'pandas')
        mg_samples_fs = pd.DataFrame.from_dict(assload.samples_in_df(df, settings.ASSNAKE_DB))
        mg_samples_fs = mg_samples_fs.merge(mg_samples, on='fs_name')
        mg_samples_fs = mg_samples_fs.to_dict(orient='records')
        return HttpResponse(json.dumps(mg_samples_fs), content_type='application/json')

class SamplesForDfFs_(APIView):
    def get(self, request, df):
        mg_samples_fs = assload.load_mg_samples_in_df_fs(settings.ASSNAKE_DB, df)
        # mg_samples_fs = pd.DataFrame.from_dict(assload.samples_in_df(df, settings.ASSNAKE_DB))
        # mg_samples_fs = mg_samples_fs.merge(mg_samples, on='fs_name')
        # mg_samples_fs = mg_samples_fs.to_dict(orient='records')
        return HttpResponse(json.dumps(mg_samples_fs), content_type='application/json')

class DatasetFullView(APIView):
    def get(self, request, df):
        preproc_dir = settings.PIPELINE_DIR + '/datasets/{df}/reads/*'
        samples_dir = settings.PIPELINE_DIR + '/datasets/{df}/reads/{preproc}/*'
        preprocs = [p.split('/')[-1] for p in glob.glob(preproc_dir.format(df=df))]

        res = []
        for p in preprocs:
            samples = [s.split('/')[-1] for s in glob.glob(samples_dir.format(df=df, preproc=p))]
            res.append({'preproc': p, 'samples': samples})

        return HttpResponse(json.dumps(res), content_type='application/json')


class TaxaGeneralCompositionView(APIView):
    def get(self, request, df, preproc, tool):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{df}/taxa/reads/{preproc}/{tool}/*/krak.tsv'
        search_dir_w_sample = datasets_dir + '{df}/taxa/reads/{preproc}/{tool}/{sample}/krak.tsv'

        search_dir = search_dir.format(df=df, preproc=preproc, tool=tool)
        search_dir_w_sample = search_dir.replace('*', '{sample}')

        meta_loc = datasets_dir + df + '/reads/meta.tsv'
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
