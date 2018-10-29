# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from celery import group
import logging
from celery import Task, states
from celery.utils.log import get_task_logger
from celery.worker.request import Request

import os
from django.conf import settings
import subprocess
from celery.worker.request import Request

from asshole.celery import app

logger = get_task_logger(__name__)
import json


def generate_snakefile(input_list, name=''):
    # Get number of files for id
    num_of_files = sum([len(files) for r, d, files in os.walk(settings.PIPELINE_DIR + '/run_snakes')])
    print('Number of files: ' + str(num_of_files))

    # Generate tmp snakemake file name
    snakefile_id = name + '.py'
    if name == '':
        snakefile_id = 'snake_run_' + str(num_of_files) + '.py'

    # Load base snakemake file
    # Read content to str
    snakefile_content = ''
    with open(settings.PIPELINE_DIR + '/bin/snake/base.py', 'r') as base:
        snakefile_content = base.read()

    # Write list of files
    snakefile_content += 'input_list=' + str(input_list) + '\n'

    # Write generated rule
    snakefile_content += '\nrule gen:\n' + '\tinput: input_list'

    # Save this string to and file to tmp folder
    snakefile_loc = settings.PIPELINE_DIR + '/run_snakes/' + snakefile_id
    with open(snakefile_loc, 'w') as file:
        file.write(snakefile_content)

    return snakefile_loc


class CallbackSnakemake(Task):

    def on_success(self, retval, task_id, args, kwargs):
        res_files = args[0]

        tasks = group([send_count.s(res) for res in res_files])
        group_task = tasks.apply_async()


@shared_task(base=CallbackSnakemake, bind=True)
def snakemake_run(self, samples_list, dry):
    sn_loc = generate_snakefile(samples_list, self.request.id)

    os.chdir(settings.PIPELINE_DIR)
    dry_arg = ''
    if dry == 1:
        dry_arg = '-n'

    p = subprocess.Popen(
        "snakemake -s " + sn_loc + " --drmaa ' -pe make 2' " + dry_arg + " -k -p --latency-wait 150 -j 2 --drmaa-log-dir ./drmaa_log gen ",
        shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()

    print('output')
    print(output)
    print('error')
    print(error)
    print('return code')
    print(p.returncode)

    ret = 'ALL DONE'
    if p.returncode != 0:
        print('BAD RETURN')
        ret = str(output)
        # self.update_state(task_id=self.request.id, state='FAILURE', meta="result is None")
        # raise let_it_fail

    return ret


@shared_task
def send_count(res):
    os.chdir(settings.PIPELINE_DIR)

    # parse loc to hard_df and sample_fs name
    if os.path.isfile(res):
        ext = (res.split('.')[-1])
        slash_split = res.split('/')

        result_lines = []
        with open(res, "r") as f:
            result_lines = f.readlines()

        data = {
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

        # Make request to MGMS and wait for response
        res_type = 'COUNTS'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        url = settings.MGMS_URL + 'api/mgms/result/' + res_type + '/'

        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r)
