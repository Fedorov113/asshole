import shutil
from django.test import TestCase, Client
from django.urls import reverse
import os
from pathlib import Path

from asshole import settings
from explorer.file_system.file_system_helpers import import_sample_file, delete_sample, get_samples_from_dir


class ImportSampleTests(TestCase):
    valid_sample_file = {'orig_file': '/data6/bio/TFM/experiments/mgs_tutorial_Oct2017/raw_data/p143N_R1.fastq.gz',
                         'df': 'TEST',
                         'sample': 'p143N',
                         'strand': 'R1'}
    invalid_sample_file = {'orig_file': '/data6/fuck/mgs_tutorial_Oct2017/raw_data/p143N_R1.fastq.gz',
                           'df': 'TEST',
                           'sample': 'p143N',
                           'strand': 'R1'}

    def tearDown(self):
        delete_sample(self.valid_sample_file)

    def valid_import_first(self):
        success, message = import_sample_file(self.valid_sample_file)
        self.assertEqual((True, 'Imported'), (success, message))

    def valid_remove(self):
        data = self.valid_sample_file
        dst_dir = settings.PIPELINE_DIR + '/datasets/{df}/reads/imp/{sample}/'
        dst_dir = dst_dir.format(
            df=data['df'],
            sample=data['sample']
        )
        delete_sample(self.valid_sample_file)
        self.assertEqual(False, os.path.isdir(dst_dir))

    def test_valid_and_remove(self):
        print('test_valid_and_remove')
        self.valid_import_first()
        self.valid_remove()

    def test_create_already_created(self):
        self.valid_import_first()
        success, message = import_sample_file(self.valid_sample_file)
        self.valid_remove()
        self.assertEqual((True, 'Already imported'), (success, message))

    def test_create_invalid_original(self):
        success, message = import_sample_file(self.invalid_sample_file)
        print(message)
        self.assertEqual((False, 'No such sample file on disk'), (success, message))


class GetSamplesFromFolderTest(TestCase):
    test_dir = os.getcwd() + '/testing_dir/'

    def setUp(self):
        os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_normal(self):
        """
        Tests {s}_R1.fastq.gz {s}_R2.fastq.gz
        """

        Path(self.test_dir + 'sample_R1.fastq.gz').touch()
        Path(self.test_dir + 'sample_R2.fastq.gz').touch()
        res = get_samples_from_dir(self.test_dir)

        self.assertEqual([{'sample_name': 'sample',
                           'files': {'R1': 'sample_R1.fastq.gz', 'R2': 'sample_R2.fastq.gz', 'S': []},
                           'renamed_files': {'R1': 'sample_R1.fastq.gz', 'R2': 'sample_R2.fastq.gz', 'S': []}}],
                         res)

    def test_001(self):
        """
        Tests {s}_R1_001.fastq.gz {s}_R2_001.fastq.gz
        """

        Path(self.test_dir + 'sample_R1_001.fastq.gz').touch()
        Path(self.test_dir + 'sample_R2_001.fastq.gz').touch()
        res = get_samples_from_dir(self.test_dir)

        self.assertEqual([{'sample_name': 'sample',
                           'files': {'R1': 'sample_R1_001.fastq.gz', 'R2': 'sample_R2_001.fastq.gz', 'S': []},
                           'renamed_files': {'R1': 'sample_R1.fastq.gz', 'R2': 'sample_R2.fastq.gz', 'S': []}}],
                         res)

    def test_1(self):
        """
        Tests {s}_1.fastq.gz {s}_2.gz
        """

        Path(self.test_dir + 'sample_1.fastq.gz').touch()
        Path(self.test_dir + 'sample_2.fastq.gz').touch()
        res = get_samples_from_dir(self.test_dir)

        self.assertEqual([{'sample_name': 'sample',
                           'files': {'R1': 'sample_1.fastq.gz', 'R2': 'sample_2.fastq.gz', 'S': []},
                           'renamed_files': {'R1': 'sample_R1.fastq.gz', 'R2': 'sample_R2.fastq.gz', 'S': []}}],
                         res)
