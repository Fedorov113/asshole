from django.test import TestCase, Client
from django.urls import reverse
import json
# initialize the APIClient app
client = Client()


class ResultRequestTests(TestCase):
    def setUp(self):
        print('setup')

    def test_centrifuge_invalid_container_request(self):
        centr_request_json_str = '{"desired_results":{"result":"centr","input_objects":["MgSampleFileContainer"],"input":[{"MgSampleFileContainer":{"df":"FHM","sample":"DFM_002_F1_S9","preproc":"imp__tmtic_def1"}}],"tool_info":{"tool":"centr","params":"def"},"threads":6,"jobs":1}}'
        response = client.post(reverse('mgms:result:result-request'), json.loads(centr_request_json_str), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_result_request_invalid_inp_obj(self):
        centr_request_json_str = '{"desired_results":{"result":"centr","input_objects":["INVALID"],"input":[{"MgSampleFileContainer":{"df":"FHM","sample":"DFM_002_F1_S9","preproc":"imp__tmtic_def1"}}],"tool_info":{"tool":"centr","params":"def"},"threads":6,"jobs":1}}'
        response = client.post(reverse('mgms:result:result-request'), json.loads(centr_request_json_str), content_type='application/json')
        self.assertEqual(response.status_code, 400)
