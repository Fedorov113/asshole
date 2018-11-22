import json
import os

import requests

from asshole import settings
import parse

from explorer.file_system.file_system_helpers import get_files_from_path_with_ext
from explorer.models import Result


class RuleSerializer:
    """ This class is used to serialize output of a rule.

    Attributes:
        rule (str): Name of the rule that produced this result.
        res_loc (str): Location of the main output file. Used to reconstruct input and output JSON objects.
    """
    def __init__(self, rule, res_loc):
        self.rule = rule
        self.res_loc = res_loc

    def serialize_mp2(self):
        os.chdir(settings.PIPELINE_DIR)  # Set working directory to pipeline root. Snake returns relative paths
        result = {'result': self.rule, 'input_objects': {}, 'raw_res': {}}  # Barebone final dict
        if os.path.isfile(self.res_loc):  # Check if file exists
            res = Result.objects.get(result_name=self.rule)  # Get corresponding Result object by ruleName from Snake

            if res.json_in_to_loc_out_func == 'simple':  # Simple dict -> wilcards
                schema = json.loads(res.input_schema)  # Load input schema
                props = list(schema['properties'].keys())  # Get keys from input schema MgSampleFileContainer

                parsed = parse.parse(res.out_str_wc, self.res_loc).named

                result['raw_res']['report'] = self.res_loc
                result['raw_res']['params'] = parsed.pop('params')
                result['input_objects'] = {props[0]: parsed}

            return result

        return None


    def serialize_tmtic(self):
        os.chdir(settings.PIPELINE_DIR) # Set working directory to pipeline root. Snake returns relative paths
        result = {'result': self.rule, 'input_objects': {}, 'raw_res': []} # Barebone final dict
        if os.path.isfile(self.res_loc): # Check if file exists
            res = Result.objects.get(result_name=self.rule) # Get corresponding Result object by ruleName from Snake

            if res.json_in_to_loc_out_func == 'simple': # Simple dict -> wildcards
                schema = json.loads(res.input_schema) # Load input schema
                props = list(schema['properties'].keys()) # Get keys from input schema MgSampleFileContainer
                # this is preproc, so we need to add tool and param if present
                parsed = parse.parse(res.out_str_wc, self.res_loc)
                print(res.out_str_wc)
                print(self.res_loc)
                parsed=parsed.named
                res_preproc = parsed['preproc'] + '__' +parsed.pop('tool')+'_'+parsed.pop('params')

                reads_files = get_files_from_path_with_ext(os.path.dirname(self.res_loc), 'fastq.gz', True)
                for rf in reads_files:
                    mg_container_file = {'MgSampleContainerFile': {
                        'df': parsed['df'],
                        'sample': parsed['sample'],
                        'preproc': res_preproc,
                        'strand': rf.rsplit('_', 1)[1]
                    }}
                    result['raw_res'].append(mg_container_file)

                result['input_objects'] = {props[0]: parsed}
            return result

        return None


    def serialize_profile(self):
        """

        :return: dict if successful, None otherwise
        """
        os.chdir(settings.PIPELINE_DIR)

        result = {'result': self.rule, 'input_objects': {}, 'raw_res': {}}
        # parse loc to hard_df and sample_fs name
        if os.path.isfile(self.res_loc):
            res = Result.objects.get(result_name=self.rule)

            if res.json_in_to_loc_out_func == 'simple':
                schema = json.loads(res.input_schema)
                props = list(schema['properties'].keys())
                parsed = parse.parse(res.out_str_wc, self.res_loc)
                result['input_objects']={props[0]:parsed.named}

            if self.res_loc.split('.')[-1] == 'tsv':
                with open(self.res_loc, 'r') as res_file:
                    for line in res_file:
                        line = line.replace('\n', '')
                        spl = line.split('\t')
                        result['raw_res'][spl[0]] = spl[1]

            return result
        return None

    def get_json(self):
        """
        This method calls serialization method 'serialize_<rule>' that converts output to dict.

        Returns:
            JSON string if successful, 'ERROR' otherwise
        """
        data = None
        fn = getattr(self, 'serialize_'+self.rule, None)
        if fn is not None:
            data = fn()

        if data is not None:
            return json.dumps(data)

    def get_dict(self):
        """
        This method calls serialization method 'serialize_<rule>' that converts output to dict.

        Returns:
            Dict if successful, 'ERROR' otherwise
        """
        data = None
        fn = getattr(self, 'serialize_'+self.rule, None)
        if fn is not None:
            data = fn()

        if data is not None:
            return data