from django.conf import settings
from .general import *
import os, glob

def getAllSeqSetsWithCategory():
    dir_with_seq_sets = os.path.join(settings.PIPELINE_DIR, 'data/ref/')
    # All folders with seq_sets i.e.:
    # data/ref/virus
    seq_sets_dirs = get_folders_in_path(dir_with_seq_sets)

    # Because it contains no seqs. Why is it even there?
    seq_sets_dirs.remove('index')

    # Now lets construct a dict {ref_type: [seq1, se2, ...], ...}
    categories_with_seq_sets = {}
    for seq_sets_dir in seq_sets_dirs:
        seq_sets_for_type = get_files_from_path_with_ext(dir_with_seq_sets+seq_sets_dir+'/', '.fa')
        categories_with_seq_sets[seq_sets_dir] = seq_sets_for_type

    print(categories_with_seq_sets)

def get_types_of_seq_sets():
    dir_with_seq_sets = os.path.join(settings.PIPELINE_DIR, 'data/ref/')
    # All folders with seq_sets i.e.:
    # data/ref/virus
    seq_sets_dirs = get_folders_in_path(dir_with_seq_sets)

    # Because it contains no seqs. Why is it even there?
    seq_sets_dirs.remove('index')

    return seq_sets_dirs

def get_seqs_for_seq_type(seq_type):
    dir_with_seq_sets = os.path.join(settings.PIPELINE_DIR, 'data/ref/')
    return get_files_from_path_with_ext(dir_with_seq_sets+seq_type+'/', '.fa')