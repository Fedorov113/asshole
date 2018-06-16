from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets

from explorer.file_system.api import serializers
from explorer.file_system.samples import get_samples_for_df_preproc
from explorer.file_system.ref_seq_explorer import *

import pandas as pd
from explorer.file_system import metaphlan2 as mp2

from rest_framework.views import APIView
import json
import explorer.file_system.helpers as hp

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


class Mp2ScatterView(APIView):
    def get(self, request):
        # THIS STUFF DOESN'T BELONG HERE!!!!
        base_dir = '/data6/bio/TFM/pipeline'
        metaphlan2_dir = '/datasets/FHM/taxa/reads/trimmomatic/metaphlan2/'
        mp2_dir = base_dir + metaphlan2_dir
        dir_strand_only = base_dir + '/datasets/FHM/taxa/reads/trimmomatic/metaphlan2/R1/'

        ext = '.mp2'
        d2t3 = {"DFM_002_F1_S9": mp2_dir + 'DFM_002_F1_S9' + ext,
                'TFM_003_F1-1_S6': mp2_dir + 'TFM_003_F1-1_S6' + ext,
                'TFM_003_F1-3_S7': mp2_dir + 'TFM_003_F1-3_S7' + ext,
                '3F5_S61': dir_strand_only + '3F5_S61' + ext}

        mp2_data = mp2.read_mp2_data(d2t3, level='f__', org='Bacteria', norm_100=True)
        mp2_data = mp2_data.reset_index().drop(['index'], axis=1)
        mp2_data = mp2_data.fillna(0)

        mp2_data_dict = mp2_data.to_dict(orient='list')
        mp2_data_json = json.dumps(mp2_data_dict)
        mp2_data_json = list(mp2_data_json)

        return HttpResponse(mp2_data_json, content_type='application/json')

class MappedView(APIView):
    def get(self, request, dataset, preproc, tool, seq_type, seq_name, postproc):
        datasets_dir = settings.PIPELINE_DIR + '/datasets/'
        search_dir = datasets_dir + '{0}/mapped/{1}/{2}/{3}/{4}/{5}/'
        search_dir = search_dir.format(dataset, preproc, tool, seq_type, seq_name, postproc)
        mapped_files = get_files_from_path_with_ext(search_dir, '.bb_stats', only_names = False)

        # remove dir to datasets
        for i, f in enumerate(mapped_files):
            mapped_files[i] = f.replace(datasets_dir, '')
            print(f)

        if len(mapped_files) > 0:
            myFiles = FileSystem(mapped_files[0])
            for i, record in enumerate(mapped_files[1:]):
                myFiles.add_child(record)

        query_params = self.request.query_params
        samples = query_params.get('samples', None)
        samples_to_plot = []

        if samples is not None:
            samples = samples.split(',')

            for i, s in enumerate(samples):
                samples[i] = s.split('.')[0]

            print(samples)
            print(search_dir)
            mapping_res = hp.load_cov_stats(samples, search_dir, '.bb_stats')
            clean_mapping_res = mapping_res
            ## leave only norm_fold for heatmap
            cols = mapping_res.columns
            for col in cols:
                if not (col == '#ID' or 'Norm_fold' in col):
                    clean_mapping_res = clean_mapping_res.drop(col, axis=1)

            # set #ID as index
            clean_mapping_res = clean_mapping_res.set_index('#ID')
            # fill NaN values with 0
            clean_mapping_res = clean_mapping_res.fillna(0)
            # drop all rowes that contain only 0
            clean_mapping_res = clean_mapping_res[(clean_mapping_res.T != 0).any()]
            clean_mapping_res_dict = clean_mapping_res.to_dict(orient='split')
            clean_mapping_res_json = json.dumps(clean_mapping_res_dict)
            clean_mapping_res_json = list(clean_mapping_res_json)

            return HttpResponse(clean_mapping_res_json, content_type='application/json')


        return HttpResponse(json.dumps(myFiles.make_dict()), content_type='application/json')


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

class ReadsView(APIView):
    def get(self, request, df, preproc):
        datasets_dir = settings.PIPELINE_DIR + '/datasets/'
        search_dir = datasets_dir + '{0}/reads/{1}/'
        search_dir = search_dir.format(df, preproc)
        read_files = get_files_from_path_with_ext(search_dir, '.bb_stats', only_names=False)

        return HttpResponse('clean_mapping_res_json', content_type='application/json')