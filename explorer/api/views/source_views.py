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
        return HttpResponse(json.dumps(assload.load_sources_in_df(df, settings.ASSNAKE_DB)), content_type='application/json')
