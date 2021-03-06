# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
import yaml
from celery import shared_task
from celery import group
import snakemake
from django_eventstream import send_event

import logging
import sys
from celery import Task, states
from celery.utils.log import get_task_logger
from celery.worker.request import Request

import os
from django.conf import settings
import subprocess
import inspect
from celery.worker.request import Request

from asshole.celery import app
from explorer.RuleSerializer import RuleSerializer
from explorer.models import SnakeRuleResult

import importlib
import select

logger = get_task_logger(__name__)
import json


# import mg_manager.result.models as result_models

def generate_snakefile(input_list, name=''):
    # Get number of files for id
    num_of_files = sum([len(files) for r, d, files in os.walk(settings.SNAKES_DIR)])
    print('Number of files: ' + str(num_of_files))

    # Generate tmp snakemake file name
    snakefile_id = name + '.py'
    if name == '':
        snakefile_id = 'snake_run_' + str(num_of_files) + '.py'

    # Load base snakemake file
    # Read content to str
    snakefile_content = ''
    with open(os.path.join(settings.ASSNAKE_INSTALLATION,'bin/templates/head.py'), 'r') as base:
        snakefile_content = base.read()

    # Add configfile
    snakefile_content += "\nconfigfile: '" + os.path.join(settings.ASSNAKE_INSTALLATION, 'config.yml') + "'"

    # Add includes
    snakefiles = "\nsnakefiles = '" + os.path.join(settings.ASSNAKE_INSTALLATION, 'bin/snake/') + "'"
    snakefile_content += snakefiles
    results = "\nresults = '" + os.path.join(settings.ASSNAKE_INSTALLATION, 'results/') + "'\n"
    snakefile_content += results

    # Add floor
    with open(os.path.join(settings.ASSNAKE_INSTALLATION,'bin/templates/floor.py'), 'r') as base:
        floor = base.read()
        snakefile_content += floor

    # Write list of files
    snakefile_content += '\ninput_list=' + str(input_list) + '\n'

    # Write generated rule
    snakefile_content += '\nrule gen:\n' + '\tinput: input_list'

    # Save this string to and file to tmp folder
    snakefile_loc = os.path.join(settings.SNAKES_DIR, snakefile_id)
    print('getting ready to save file')
    with open(snakefile_loc, 'w') as file:
        file.write(snakefile_content)

    return snakefile_loc


class CallbackSnakemake(Task):

    def on_success(self, retval, task_id, args, kwargs):
        results = list(SnakeRuleResult.objects.filter(task_id=task_id))
        print('IN CALLBACK' + task_id)
        # for res in results:
        # print('printing result')
        # print(res.rule_name)
        # print(res.output_to_serialize)

        tasks = group([ser_and_send_to_m.s(res.rule_name, res.output_to_serialize) for res in results])
        group_task = tasks.apply_async()


def snake_log(log_dict):
    print(log_dict)
    send_event('test', 'message', log_dict)


@shared_task(base=CallbackSnakemake, bind=True)
def snakemake_run(self, samples_list, dry, threads=1, jobs=1):
    sn_loc = generate_snakefile(samples_list, self.request.id)

    print('task_id ' + str(self.request.id))

    os.chdir(settings.PIPELINE_DIR)
    dry_arg = ''
    if dry == 1:
        dry_arg = '-n'
        print('running dry')

    configfile = os.path.join(settings.ASSNAKE_INSTALLATION, 'config.yml')
    conda_prefix = ''
    with open(configfile) as f:
        config = yaml.load(f)
        conda_prefix = config['conda_prefix']

    status = 1
    status = snakemake.snakemake(sn_loc,
                                 config=dict(assnake_install_dir=settings.ASSNAKE_INSTALLATION),
                                 targets=['gen'],
                                 printshellcmds=True,
                                 dryrun=True,
                                 configfile=os.path.join(settings.ASSNAKE_INSTALLATION, 'config.yml'),
                                 use_conda=True,
                                 conda_prefix=conda_prefix,
                                 log_handler=snake_log,
                                 latency_wait = 350,
                                 quiet = True
                                 )
    # shell_cmd_wc = "/data6/bio/TFM/soft/miniconda3/envs/snake/bin/snakemake -s {sn_loc} --cluster 'qsub' {dry} -k -p --latency-wait 150 -j {jobs}  gen --config task_id='{task_id}'"
    #
    # shell_cmd_wc = """/data6/bio/TFM/soft/miniconda3/envs/snake/bin/snakemake -s {sn_loc} \
    # --drmaa ' -pe make {threads}' {dry} -k -p --latency-wait 150 -j {jobs} \
    # --drmaa-log-dir ./drmaa_log gen --config task_id='{task_id}'"""
    #
    # shell_cmd = shell_cmd_wc.format(sn_loc=sn_loc, dry=dry_arg, threads=threads, jobs=jobs, task_id=self.request.id)
    #
    # print('OPENING SUBPROCESS')
    # p = subprocess.Popen(
    #     shell_cmd,
    #     shell=True,
    #     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    # def check_io():
    #     ready_to_read = select.select([p.stdout, p.stderr], [], [], 1000)[0]
    #     for io in ready_to_read:
    #         line = io.readline()
    #         print(line)
    #         # logger.info(line[:-1])
    #
    # # keep checking stdout/stderr until the child exits
    # while p.poll() is None:
    #     check_io()
    #
    # check_io()
    #
    # output, error = p.communicate()
    #
    # if p.returncode != 0:
    #     print('!!!!!ERROR!!!!!')
    #     print(error)
    #     print('return code')
    #     print(p.returncode)
    # else:
    #     print('output')
    #     print(output)
    #
    # ret = 'ALL DONE'
    # if p.returncode != 0:
    #     print('BAD RETURN')
    #     ret = str(output)
    #     # self.update_state(task_id=self.request.id, state='FAILURE', meta="result is None")
    #     # raise let_it_fail

    return status


@shared_task
def ser_and_send_to_m(rule_name, rule_result):
    print(rule_result)
    ser = RuleSerializer(rule_name, rule_result)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    url = settings.ASSHOLE_URL + 'api/mgms/result/'
    r = requests.post(url, data=json.dumps(ser.get_dict()), headers=headers)
    print(r)
