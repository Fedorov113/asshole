from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, status

from . import serializers
from .samples import get_samples_for_df_preproc
from .ref_seq_explorer import *

import pandas as pd
from . import metaphlan2 as mp2
from rest_pandas import PandasSimpleView

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
import json

class SampleFSViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.SampleFSSerializer

    def list(self, request):
        samples = get_samples_for_df_preproc('FHM', 'raw')
        print(samples)
        ss = {'sample_name':samples}
        serializer = serializers.SampleFSSerializer(
            instance=ss)
        return Response(serializer.data)

class Mp2View(APIView):
    def get(self, request):
        # Read level and adjust it for mp2
        level = self.request.query_params.get('level')
        if level is not None:
            level += '__'
        else:
            level = 'f__'

        # THIS STUFF DOESN'T BELONG HERE!!!!
        base_dir = '/data6/bio/TFM/pipeline'
        metaphlan2_dir = '/datasets/FHM/taxa/reads/trimmomatic/metaphlan2/'
        mp2_dir = base_dir + metaphlan2_dir
        dir_strand_only = base_dir + '/datasets/FHM/taxa/reads/trimmomatic/metaphlan2/R1/'

        ext = '.mp2'

        samples = ["DFM_002_F1_S9", 'DFM_2F2_S62']
        FHM_hand = ['3F5_S61', '5F1_S44', '5F2_S45', '5F3_S46', '6F1_S47', '6F2_S48',
                    '6F3_S49', '6F4_S50', '7F1_S51', '7F2_S52', '7F3_S53', '8F2_S55',
                    '8F3_S56', '9F1_S57', '9F2_S58', '9F3_S59']

        samples_meta = pd.read_csv(base_dir + '/datasets/FHM/reads/meta.tsv', sep='\t')

        samples_loc = {}
        for s in samples:
            samples_loc[s] = mp2_dir + s + ext

        mp2_data = mp2.read_mp2_data(samples_loc, level=level, org='Bacteria')
        mp2_data = mp2_data.reset_index().drop(['index'], axis=1)
        mp2_data = mp2_data.fillna(0)

        mp2_data_dict = mp2_data.to_dict(orient='list')
        mp2_data_json = json.dumps(mp2_data_dict)
        mp2_data_json = list(mp2_data_json)

        return HttpResponse(mp2_data_json, content_type='application/json')


class RefSeqSetsView(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.RefSeqSetsSerializer

    def list(self, request):
        types = get_types_of_seq_sets()
        categories_with_seq_sets = []
        for seq_type in types:
            seqs_for_type = get_seqs_for_seq_type(seq_type)
            data = {'type': seq_type, 'seqs': seqs_for_type}
            categories_with_seq_sets.append(data)

        print(categories_with_seq_sets)
        serializer = serializers.RefSeqSetsSerializer(
            instance=categories_with_seq_sets, many=True)
        return Response(serializer.data)