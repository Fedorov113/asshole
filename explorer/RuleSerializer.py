import json
import os

import requests

from asshole import settings


class RuleSerializer:

    def __init__(self, rule, res_loc):
        self.rule = rule
        self.res_loc = res_loc

    def serialize_count(self):
        os.chdir(settings.PIPELINE_DIR)

        # parse loc to hard_df and sample_fs name
        if os.path.isfile(self.res_loc):
            ext = (self.res_loc.split('.')[-1])
            if ext == 'count':
                slash_split = self.res_loc.split('/')

                result_lines = []
                with open(self.res_loc, "r") as f:
                    result_lines = f.readlines()

                data = {
                    'rule': self.rule,
                    'input': {
                        'name_on_fs': slash_split[-2],
                        'df': slash_split[1],
                        'preproc': slash_split[3],
                        'strand': slash_split[-1].split('.')[0].split('_')[-1],
                    },
                    'result': {
                        'reads': int(result_lines[0][0:-2].split(' ')[0]),
                        'bp': int(result_lines[0][0:-2].split(' ')[1])
                    }
                }

                return json.dumps(data)
        return 0



    def to_json(self):
        fn = getattr(self, 'serialize_'+self.rule, None)
        if fn is not None:
            fn(self.res_loc)