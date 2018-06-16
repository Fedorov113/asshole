import os, glob
from django.conf import settings
from .file_system_helpers import *

STRAND = '_R1'
EXT = '.fastq.gz'

def get_samples_for_df(df_name, preproc, batch_id):
    """
    Returns list of dictionaries of format {preproc_name: [sample1, ...]}
    :param df_name:
    :param preproc:
    :param batch_id:
    :return:
    """
    # preproc can be a list for several, str for one, all for all
    # it is string

    # Get all preprocess reads folder for this dataset
    reads_dir = os.path.join(settings.PIPELINE_DIR, 'datasets/'
                             + df_name
                             + '/reads/')
    dirs_with_reads = get_folders_in_path(reads_dir)


    sample_files_dir = reads_dir + '%s/'
    preproc_files = {}
    for preproc_dir in dirs_with_reads:
        directory = sample_files_dir % preproc_dir

        # If
        if len(glob.glob(directory + sample_name + '*.fastq.gz')) > 0:
            reads_files = get_files_from_path_with_ext(directory + sample_name, '.fastq.gz')
            reads_files.sort()

            reads_files_info = []
            for file in reads_files:
                f_size = os.stat(directory + file + '.fastq.gz').st_size
                reads_files_info.append([file, sizeof_fmt(f_size)])
            print(reads_files_info)
            preproc_files[dir] = reads_files_info

    df_raw_reads_path = os.path.join(settings.PIPELINE_DIR, 'datasets/'
                                     + df_name
                                     + '/reads/'+preproc+'/')

    df_files = [
        item.split("/")[-1].split(STRAND + EXT)[0]
        for item in glob.glob(df_raw_reads_path + '*' + STRAND + EXT)
    ]

    df_files.sort()
    return df_files

def get_samples_for_df_preproc(df_name, preproc, full_path = False):
    """
    Returns list of
    :param df_name:
    :param preproc:
    :param batch_id:
    :return:
    """
    reads_dir = os.path.join(settings.PIPELINE_DIR, 'datasets/'
                             + df_name
                             + '/reads/')
    sample_files_dir = reads_dir + preproc + '/'

    samples_in_dir = []

    # Such dir exists
    if os.path.isdir(sample_files_dir):
        fqgz_files_in_dir = glob.glob(sample_files_dir+'*.fastq.gz')
        # It contains fastq gz files
        if len(fqgz_files_in_dir) > 0:
            # Now get only sample names (one sample can have up to 3 files).
            # Assuming that files end on ['_R1', '_R2, '_S'] or nothing from that
            with_R1 = glob.glob(sample_files_dir+'*'+STRAND + EXT)
            if len(with_R1) > 0:
                print( "contains files with _R1" )
                if full_path:
                    pass
                else:
                    samples_in_dir = [
                        item.split("/")[-1].split(STRAND + EXT)[0]
                        for item in with_R1
                    ]
            else:
                samples_in_dir = [
                    item.split("/")[-1].split(EXT)[0]
                    for item in fqgz_files_in_dir
                ]

    samples_in_dir.sort()
    return samples_in_dir


















            # reads_files = get_files_from_path_with_ext(directory + sample_name, '.fastq.gz')
            # reads_files.sort()
            #
            # reads_files_info = []
            # for file in reads_files:
            #     f_size = os.stat(directory + file + '.fastq.gz').st_size
            #     reads_files_info.append([file, sizeof_fmt(f_size)])
            # print(reads_files_info)
            # preproc_files[dir] = reads_files_info