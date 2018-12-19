import os

from celery import uuid
from celery.worker.state import requests
import requests as req
from asshole import settings
from explorer.RuleSerializer import RuleSerializer
from explorer.models import Result
from explorer.tasks import snakemake_run
import json


def create_simple_wc(out_wc, tool_info, input_object, input_object_name):
    dict_to_expand = {}
    if tool_info is not None:
        dict_to_expand = tool_info.copy()
    dict_to_expand.update(input_object[input_object_name[0]])
    return out_wc.format(**dict_to_expand)


def check_if_result_computed(result, res_loc):
    """
    Checks if result is computed. If it is - sends it to Management System
    :param result: Name of result
    :param res_loc: Location of result file
    :return: True if computed, False otherwise
    """
    if os.path.isfile(settings.PIPELINE_DIR + '/' + res_loc):  # THIS RESULT WAS ALREADY COMPUTED
        ser = RuleSerializer(result, res_loc)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        url = settings.ASSHOLE_URL + 'api/mgms/result/'
        r = req.post(url, data=ser.get_json(), headers=headers)
        print(r)
        return True
    else:
        return False


def create_many_containers_from_wc(out_wc, tool_info, input_object, input_object_name):
    if tool_info is None:
        return 0

    dict_to_expand = tool_info.copy()
    many_containers_from_df = ''
    rrr = []
    for cont in input_object['ArrayOfMgSampleContainer']:
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
        dfs += df + '+'
        for i, pr in enumerate(r[df]):
            preproc = list(pr.keys())[0]
            preprocs += preproc + '='
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

    dict_to_expand['dfs'] = dfs
    dict_to_expand['preprocs'] = preprocs
    dict_to_expand['samples'] = samples
    print(dict_to_expand)
    # dict_to_expand.update(inp[input_objects[0]])

    out_loc = out_wc.format(**dict_to_expand)
    return out_wc.format(**dict_to_expand)


NO_RESULT_IN_DB = 1


def generate_files_for_snake_from_request_dict(request_dict):
    """
    Takes dictionary and returns list of files for snakemake

    :param request_dict: { input: [], input_objects: ['MgSampleFile'], result: 'profile" }
    :return: list with file locations if everything is OK, integer error code otherwise
    """
    input_loc_list = []  # list of files to request from snakemake
    desired = request_dict['desired_results']

    # Trying to get desired result from db.
    try:
        res = Result.objects.get(result_name=desired['result'])
    except Result.DoesNotExist:
        return NO_RESULT_IN_DB

    if res.json_in_to_loc_out_func == 'simple':
        for inp in desired['input']:
            out_loc = create_simple_wc(res.out_str_wc, desired.get('tool_info'), inp, desired.get('input_objects'))
            if not check_if_result_computed(desired['result'], out_loc):
                input_loc_list.append(out_loc)

    elif res.json_in_to_loc_out_func == 'many_containers':
        for inp in desired['input']:
            out_loc = create_many_containers_from_wc(res.out_str_wc, desired.get('tool_info'), inp,
                                                     desired.get('input_objects'))
            if not os.path.isfile(out_loc):
                input_loc_list.append(out_loc)

    return input_loc_list
