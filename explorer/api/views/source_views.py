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

class SourcesForDfFs(APIView):
    def get(self, request, df):
        sources = assload.load_sources_in_df(df, settings.ASSNAKE_DB)

        sources_w_schemas = glob.glob(settings.ASSNAKE_DB+'/datasets/{df}/sources__*.tsv'.format(df=df))
        if len(sources_w_schemas) > 0:
            sources_meta = pd.read_csv(sources_w_schemas[0], sep = '\t')
            sources_meta = sources_meta.fillna('null')

            for s in sources:
                info = sources_meta.loc[sources_meta['source'] == s['source']]
                s.update({'meta_info': info.loc[:, info.columns != 'source'].to_dict(orient='records')[0]})
        else:
            for s in sources:
                s.update({'meta_info': {}})

        return HttpResponse(json.dumps(sources), content_type='application/json')
