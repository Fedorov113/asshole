# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging
from celery.utils.log import get_task_logger

import os
from django.conf import settings
import subprocess



@shared_task
def add(x, y):
    print(x + y)
    return x + y

@shared_task
def snakemake_run(sn_loc, dry):
    os.chdir(settings.PIPELINE_DIR)
    dry_arg = ''
    if dry == 1:
        dry_arg = '-n'

    # subprocess.run("snakemake -s "+sn_loc+" --drmaa ' -pe make 2' "+dry_arg+" -k -p --latency-wait 150 -j 2 --drmaa-log-dir ./drmaa_log gen ",
    #                shell=True)
    p = subprocess.Popen("snakemake -s "+sn_loc+" --drmaa ' -pe make 2' "+dry_arg+" -k -p --latency-wait 150 -j 2 --drmaa-log-dir ./drmaa_log gen ",
                     shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()

    logger = get_task_logger(__name__)
    logger.debug("SOME OUTPUT HERE")

    print('output')
    print(output)
    print('error')
    print(error)
    print('return code')
    print(p.returncode)
    return 'run?'
