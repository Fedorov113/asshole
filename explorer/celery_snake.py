import os

from celery import uuid
from celery.worker.state import requests
import requests as req
from asshole import settings
from explorer.RuleSerializer import RuleSerializer
from explorer.models import Result
from explorer.tasks import snakemake_run
import json


def run_snakemake_from_dict(request_dict):
    """

    :param request_dict: { input: [], input_objects: ['MgSampleFile'], result: 'profile" }
    :return:
    """
    task_id = uuid()
    desired = request_dict['desired_results']

    # create out_loc from JSON
    res = Result.objects.get(result_name=desired['result'])

    input_loc_list = []
    if res.json_in_to_loc_out_func == 'simple':
        out_wc = res.out_str_wc
        input_objects = desired['input_objects']
        tool_info = {}

        if 'tool_info' in desired.keys():
            tool_info = desired['tool_info']

        for inp in desired['input']:
            dict_to_expand = tool_info.copy()
            dict_to_expand.update(inp[input_objects[0]])
            out_loc = out_wc.format(**dict_to_expand)


            if os.path.isfile(settings.PIPELINE_DIR + '/' + out_loc):
                # THIS FILE WAS ALREADY COMPUTED
                print(out_loc)
                ser = RuleSerializer(desired['result'], out_loc)
                headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
                url = settings.ASSHOLE_URL + 'api/mgms/result/'
                r = req.post(url, data=ser.get_json(), headers=headers)
                print(r)
            input_loc_list.append(out_loc)
    elif res.json_in_to_loc_out_func == 'many_containers_from':
        out_wc = res.out_str_wc
        input_objects = desired['input_objects']
        tool_info = {}

        if 'tool_info' in desired.keys():
            tool_info = desired['tool_info']
            for inp in desired['input']:
                dict_to_expand = tool_info.copy()
                many_containers_from_df = ''
                rrr = []
                for cont in inp['ArrayOfMgSampleContainer']:
                    if len(rrr) == 0:
                        rrr.append({cont['df']: [{cont['preproc']: [cont['sample']]}]})

                    for j, r in enumerate(rrr):
                        if cont['df'] in r.keys():
                            for i, pr in enumerate(r[cont['df']]):
                                if cont['preproc'] in pr.keys():
                                    if cont['sample'] not in pr[cont['preproc']]:
                                        rrr[j][cont['df']][i][cont['preproc']].append(cont['sample'])
                                else:
                                    rrr[j][cont['df']].append({cont['preproc']: [cont['sample']]})
                        else:
                            rrr.append({cont['df']: [{cont['preproc']: [cont['sample']]}]})
                dfs = ''
                preprocs = ''
                samples = ''
                for r in rrr:
                    df = list(r.keys())[0]
                    dfs += df+'+'
                    for i, pr in enumerate(r[df]):
                        preproc = list(pr.keys())[0]
                        preprocs += preproc+'='
                        for s in pr[preproc]:
                            samples += s + ':'
                        samples = samples[0:-1]
                        samples += '='
                    preprocs = preprocs[0:-1]
                    samples = samples[0:-1]
                    preprocs += '+'
                    samples += '+'
                    many_containers_from_df += '+'
                preprocs = preprocs[0:-1]
                samples = samples[0:-1]
                dfs = dfs[0:-1]

                dict_to_expand['dfs']=dfs
                dict_to_expand['preprocs']=preprocs
                dict_to_expand['samples']=samples
                print(dict_to_expand)
                # dict_to_expand.update(inp[input_objects[0]])

                out_loc = out_wc.format(**dict_to_expand)
                if not os.path.isfile(out_loc):
                #THIS FILE WAS NOT ALREADY COMPUTED
                    input_loc_list.append(out_loc)

    print(input_loc_list)

    snakemake_run.apply_async((input_loc_list, 0, desired['threads'], 42), task_id=task_id)
