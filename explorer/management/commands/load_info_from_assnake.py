import glob
import json

import pandas as pd
from django.core.management.base import BaseCommand
from explorer.models import ResultType, Result

assnake_loc = '/data6/bio/TFM/pipeline/assnake'



class Command(BaseCommand):
    help = 'Imports data about results, result types and input objects from assnake'

    def handle(self, *args, **options):

        result_types = pd.read_csv(assnake_loc + '/results/result_types.tsv', sep='\t')
        result_types = result_types.to_dict(orient='records')
        for result_type in result_types:
            res = ResultType(**result_type)
            res.save()

        results = glob.glob(assnake_loc+'/results/*/*.json')

        for result in results:
            with open(result) as result_file:
                result_dict = json.load(result_file)
                res_type = ResultType.objects.get(id=result_dict['result_type'])
                result_dict['result_type'] = res_type
                result_dict.pop('params_schema')
                result_dict.pop('tool')
                result_dict['input_schema'] = json.dumps(result_dict['input_schema'])
                Result(**result_dict).save()
