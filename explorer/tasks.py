# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import os
from django.conf import settings
import subprocess


@shared_task
def add(x, y):
    print(x + y)
    return x + y

@shared_task
def snakemake_run(input_list):
    os.chdir(settings.PIPELINE_DIR)

    subprocess.run("snakemake --drmaa ' -pe make 2' -k -p --latency-wait 150 -j 2 --drmaa-log-dir ./myyy gen ", shell=True)
    # logger = Logger()
    # logger.setup_logfile()
    # #setup_logger(handler=logger.logfile_handler)
    #
    # print(logger.logfile_handler )
    #
    # workflow = Workflow(__file__,restart_times=2)
    # #snakemake.workflow.rules = Rules()
    # #snakemake.workflow.config = dict()
    #
    # workflow.configfile('/data6/bio/TFM/pipeline/config.yml')
    #
    # # snakefiles = os.path.join(workflow.config["software"]["snakemake_folder"], "bin/snake/")
    #
    # snakefiles = settings.PIPELINE_DIR+'/bin/snake/'
    #
    # workflow.include(snakefiles + "bowtie2.py")
    # workflow.include(snakefiles + "anvio.py")
    # workflow.include(snakefiles + "prokka.py")
    # workflow.include(snakefiles + "bwa.py")
    # workflow.include(snakefiles + "megahit.py")
    # workflow.include(snakefiles + "general.py")
    # workflow.include(snakefiles + "preprocess.py")
    # workflow.include(snakefiles + "marker")
    # workflow.include(snakefiles + "taxa.py")
    # workflow.include(snakefiles + "strain_finder.py")
    # workflow.include(snakefiles + "download.py")
    #
    # workflow.check()
    #
    # @workflow.rule(name='generated_rule', lineno=50, snakefile='.../Snakefile')
    # @workflow.input(
    #     input_list
    # )
    # @workflow.norun()
    # @workflow.run
    # def __rule_generated_rule(input, output, params, wildcards, threads, resources, log, version, rule, conda_env,
    #                           singularity_img, singularity_args, use_singularity, bench_record, jobid, is_shell):
    #     pass
    #
    # workflow.check()
    # print("Dry run first ...")
    # workflow.execute(dryrun=False,
    #                  updated_files=[],
    #                  unlock=False,
    #                  drmaa=' -pe make 2',
    #                  cores=2,
    #                  drmaa_log_dir='./my_log',
    #                  jobname='snakejob.{rulename}.{jobid}.sh',
    #                  resources=dict(),
    #                  latency_wait=150,
    #                  printshellcmds=True,
    #                  force_use_threads=True,
    #                  max_status_checks_per_second=1)

    return 'run?'
