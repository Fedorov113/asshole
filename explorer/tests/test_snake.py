from django.test import TestCase, Client
from django.urls import reverse
import json

from explorer.celery_snake import generate_files_for_snake_from_request_dict
from explorer.models import *


class SnakemakeFromDictTests(TestCase):
    def setUp(self):
        print('setup')
        taxa_type = ResultTypes.objects.create(result_type='taxa', description='')
        Result.objects.create(
            data_type='wgs', result_name='centr', result_type=taxa_type,
            out_str_wc='datasets/{df}/taxa/{preproc}/centr__{params}/{sample}/{sample}_krak.tsv',
            json_in_to_loc_out_func='simple', input_schema='{}', tool_params_schema='{}')

    def test_unknown_result(self):
        uncknown_request_json_str = '{"desired_results":{"result":"fuck","input_objects":["MgSampleFileContainer"],"input":[{"MgSampleFileContainer":{"df":"FHM","sample":"DFM_002_F1_S9","preproc":"imp__tmtic_def1"}}],"tool_info":{"tool":"centr","params":"def"},"threads":6,"jobs":1}}'
        dd = json.loads(uncknown_request_json_str)
        res = generate_files_for_snake_from_request_dict(dd)  # expect 1 - code for undefined result
        self.assertEqual(res, 1)

    def test_cent_not_computed(self):
        centr_request_json_str = '{"desired_results":{"result":"centr","input_objects":["MgSampleFileContainer"],"input":[{"MgSampleFileContainer":{"df":"FHM","sample":"TEST","preproc":"imp"}}],"tool_info":{"tool":"centr","params":"def"},"threads":6,"jobs":1}}'
        dd = json.loads(centr_request_json_str)
        res = generate_files_for_snake_from_request_dict(dd)  # expect 1 - code for undefined result
        self.assertEqual(res, ['datasets/FHM/taxa/imp/centr__def/TEST/TEST_krak.tsv'])
