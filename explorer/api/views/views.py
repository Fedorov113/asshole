from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets

from explorer.api import serializers
from explorer.file_system.samples import get_samples_for_df_preproc
from explorer.file_system.ref_seq_explorer import *
from explorer.file_system.file_system_class import ReadsInSystem


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
        ss = {'sample_name': samples}
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


class Mp2BoxView(APIView):
    def get(self, request, dataset, preproc):
        mp2_dir = settings.PIPELINE_DIR + '/datasets/'
        mp2_dir += '{df}/taxa/reads/{preproc}/mp2/'
        mp2_dir = mp2_dir.format(df=dataset, preproc=preproc)

        return 0


class DatasetsFSView(APIView):
    def get(self, request):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/*'
        datasets_folders = glob.glob(datasets_dir)
        print(datasets_folders)

        rifs = ReadsInSystem(pipeline_dir, datasets_folders[0].replace(pipeline_dir, ''))

        for i, record in enumerate(datasets_folders[1:]):
            record = record.replace(pipeline_dir, '')
            rifs.add_child(pipeline_dir, record)

        print('LETS SEE WHAT WEVE GOT')
        print(rifs.__str__())

        df_list = []
        for df in datasets_folders:
            df_list.append(df.replace(pipeline_dir + 'datasets/', ''))

        return HttpResponse(json.dumps(df_list), content_type='application/json')


class DatasetPreprocsAPIVIew(APIView):
    def get(self, request, df):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        preprocs_dir = pipeline_dir + 'datasets/' + df + '/reads/*'
        preprocs = glob.glob(preprocs_dir)

        preprocs_list = []
        for preproc in preprocs:
            if os.path.isdir(preproc):
                preprocs_list.append(preproc.replace(pipeline_dir + 'datasets/' + df + '/reads/', ''))

        return HttpResponse(json.dumps(preprocs_list), content_type='application/json')


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


class Mp2BoxAPIView(APIView):
    def get(self, request):
        # Parse query
        query_params = self.request.query_params
        df = query_params.get('df', None)
        preproc = query_params.get('preproc', None)
        samples = query_params.get('samples', None)

        # Construct paths to load data
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        mp2_dir = datasets_dir + '{df}/taxa/reads/{preproc}/mp2/'
        mp2_dir_for_df_preproc = mp2_dir.format(df=df, preproc=preproc)
        mp2_files = glob.glob(mp2_dir_for_df_preproc + '*.mp2')
        # Dictionary of format {sample_name: file_location}
        samples_loc = {}
        for file in mp2_files:
            samples_loc[file.split('/')[-1].replace('.mp2', '')] = file

        # Load Data
        mp2_data = mp2.read_mp2_data(samples_loc, level='o__', org='Bacteria', norm_100=False)
        mp2box = mp2_data.set_index('sample').T
        mp2box = mp2box.fillna('none')
        # Transform to json
        mp2_box_dict = mp2box.to_dict(orient='index')
        # mp2_box_json = json.dumps(mp2_box_dict)
        # mp2_box_json = list(mp2_box_json)
        final_dict = {'df': df, "preproc": preproc, 'mp2box': mp2_box_dict}
        return HttpResponse(json.dumps(final_dict), content_type='application/json')


class MappedView(APIView):

    def get(self, request, dataset, preproc, tool, seq_type, seq_name, postproc):
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = settings.PIPELINE_DIR + '/datasets/'
        search_dir = datasets_dir + '{0}/mapped/{1}/{2}/{3}/{4}/{5}/'
        search_dir = search_dir.format(dataset, preproc, tool, seq_type, seq_name, postproc)
        mapped_files = get_files_from_path_with_ext(search_dir, '.bb_stats', only_names=False)

        # remove dir to datasets
        for i, f in enumerate(mapped_files):
            mapped_files[i] = f.replace(settings.PIPELINE_DIR + '/', '')

        mapped = ReadsInSystem(pipeline_dir, mapped_files[0])

        if len(mapped_files) > 0:
            myFiles = FileSystem(mapped_files[0])
            for i, record in enumerate(mapped_files[1:]):
                myFiles.add_child(record)
                mapped.add_child(pipeline_dir, record)

        query_params = self.request.query_params
        samples = query_params.get('samples', None)
        query_filter = query_params.get('filter', None)

        if samples is not None:
            samples = samples.split(',')
            for i, s in enumerate(samples):
                samples[i] = s.split('.')[0]
            query_string = ''
            print(samples)
            print(search_dir)
            mapping_res = hp.load_cov_stats(samples, search_dir, '.bb_stats')

            # apply filter if exists
            if query_filter is not None and query_filter != '':
                print(query_filter)
                query_filter = query_filter.replace('and', '&')
                query_filter = query_filter.replace('or', '|')
                for sample in samples:
                    query_string += query_filter.format(s=sample)
                query_string = query_string[0:-3]
                print(query_string)
                mapping_res = hp.get_df_from_query(mapping_res, query_string)

            ## leave only norm_fold for heatmap
            cols = mapping_res.columns
            for col in cols:
                if not (col == '#ID' or 'Norm_fold' in col):
                    mapping_res = mapping_res.drop(col, axis=1)

            # # Only with hosts
            # vir_info_loc = '/data6/bio/TFM/pipeline/data/ref/virus/IMGVR_mVCs_nucleotides.info.tsv'
            # vir_info = pd.read_csv(vir_info_loc, sep='\t', low_memory=False)
            # with_hosts = vir_info.loc[vir_info['Host'].notna()]
            # with_hosts_list = list(with_hosts['mVCs'])
            # mapping_res = mapping_res.loc[mapping_res['#ID'].isin(with_hosts_list)]

            # set #ID as index
            mapping_res = mapping_res.set_index('#ID')
            # fill NaN values with 0
            mapping_res = mapping_res.fillna(0)
            # drop all rowes that contain only 0
            # clean_mapping_res = clean_mapping_res[(clean_mapping_res.T != 0).any()]
            cols = mapping_res.columns
            rename_cols = {}
            for i, col in enumerate(cols):
                rename_cols[col] = col.replace('Norm_fold__', '')
            clean_mapping_res = mapping_res.rename(rename_cols, axis='columns')

            clean_mapping_res_dict = clean_mapping_res.to_dict(orient='split')
            clean_mapping_res_json = json.dumps(clean_mapping_res_dict)
            clean_mapping_res_json = list(clean_mapping_res_json)

            return HttpResponse(clean_mapping_res_json, content_type='application/json')

        return HttpResponse(json.dumps(mapped.to_dict()), content_type='application/json')


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
        pipeline_dir = settings.PIPELINE_DIR + '/'
        datasets_dir = pipeline_dir + 'datasets/'
        search_dir = datasets_dir + '{0}/reads/{1}/'
        search_dir = search_dir.format(df, preproc)
        read_files = glob.glob(search_dir + '*/*.fastq.gz')
        read_files.sort()
        print(read_files)
        rifs = ReadsInSystem(pipeline_dir, read_files[0].replace(pipeline_dir, ''))

        for i, record in enumerate(read_files[1:]):
            record = record.replace(pipeline_dir, '')
            rifs.add_child(pipeline_dir, record)

        return HttpResponse(json.dumps(rifs.to_dict()), content_type='application/json')


class CheckSamplesInFolder(APIView):
    def get(self, request):
        query_params = self.request.query_params
        loc = query_params.get('loc', None)

        samples = get_samples_from_dir(loc)

        return HttpResponse(json.dumps(samples), content_type='application/json')
