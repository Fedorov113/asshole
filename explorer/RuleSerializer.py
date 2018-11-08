import json
import os

import requests

from asshole import settings
import parse

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

    def serialize_profile(self):
        """

        :return: dict if successful, None otherwise
        """
        os.chdir(settings.PIPELINE_DIR)

        result = {'result': self.rule, 'input': {}, 'raw_res': {}}
        # parse loc to hard_df and sample_fs name
        if os.path.isfile(self.res_loc):
            res = Result.objects.get(result_name=self.rule)

            if res.json_in_to_loc_out_func == 'simple':
                schema = json.loads(res.input_schema)
                props = list(schema['properties'].keys())


                parsed = parse.parse(res.out_str_wc, self.res_loc)
                result['input']={props[0]:parsed.named}

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