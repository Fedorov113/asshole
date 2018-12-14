from django.db import models
import json
from ..models import MgFile, MgSampleFileContainer, MgSample, DatasetHard


def get_df(df):
    try:
        df = DatasetHard.objects.get(df_name=df)
        return df
    except DatasetHard.DoesNotExist:
        print('NO DATASET WITH NAME {df}'.format(df=df))


def get_mg_sample(df, sample):
    try:
        sample = MgSample.objects.get(
            name_on_fs=sample,
            dataset_hard__df_name=df
        )
        return sample
    except MgSample.DoesNotExist:
        print('NO SAMPLE FROM {df} WITH NAME {sample}'.format(df=df, sample=sample))
        return None


def get_mg_sample_container(df, sample, preproc, create=False):
    try:
        cont = MgSampleFileContainer.objects.get(
            preprocessing=preproc,
            mg_sample__name_on_fs=sample,
            mg_sample__dataset_hard__df_name=df
        )
        return cont
    except MgSampleFileContainer.DoesNotExist:
        if create:
            sample = get_mg_sample(df, sample)
            if sample is not None:
                cont = MgSampleFileContainer(mg_sample=sample, preprocessing=preproc)
                cont.save()
                return cont
    return None


def get_mg_sample_container_file(df, sample, preproc, strand, create=False):
    try:
        mg_file = MgFile.objects.get(
            strand=strand,
            container__preprocessing=preproc,
            container__mg_sample__name_on_fs=sample,
            container__mg_sample__dataset_hard__df_name=df,
        )
        return mg_file
    except MgFile.DoesNotExist:
        if create:
            cont = get_mg_sample_container(df, sample, preproc, create)
            if cont is not None:
                mg_file = MgFile(container=cont, strand=strand)
                mg_file.save()
                return mg_file
    return None


class GeneralResult:
    name = ''
    # DICT representation of input
    input_objects = {}
    # JSON - stored only if no specific model is defined
    raw_res = ''

    def __init__(self, name, input_objects, raw_res):
        self.name = name
        self.input_objects = input_objects
        self.raw_res = raw_res

    def save(self):
        print('-NAME----- ' + self.name)

        # Create new instance of that model
        # TODO cannot just expand this. Should we override save, or create a specific function inside model class?
        # For now I will use another hack
        if self.name == 'tmtic':
            # input_obj = self.input_objects['MgSampleFile']
            res_dict = json.loads(self.raw_res)
            print(res_dict)
            for res_obj in res_dict:
                res = res_obj['MgSampleContainerFile']
                print(
                    get_mg_sample_container_file(res['df'], res['sample'], res['preproc'], res['strand'], create=True))

            pass
        elif self.name == 'mp2':
            print('IN MP2')
            result_model = globals()[self.name.capitalize() + 'Result']
            result_instance = result_model(**json.loads(self.raw_res))
            input_obj = self.input_objects['MgSampleFileContainer']
            cont = get_mg_sample_container(**input_obj)
            result_instance.mg_container = cont
            result_instance.save()

        elif self.name == 'profile':
            # Get class corresponding to result: <Name>Result
            result_model = globals()[self.name.capitalize() + 'Result']

            input_obj = self.input_objects['MgSampleFile']
            input_obj = MgFile.objects.get(
                strand=input_obj['strand'],
                container__preprocessing=input_obj['preproc'],
                container__mg_sample__name_on_fs=input_obj['sample'],
                container__mg_sample__dataset_hard__df_name=input_obj['df']
            )
            mg_file = input_obj

            # Try to get this result, if there is no such - save
            try:
                result_model.objects.get(mg_file=mg_file)
                print('result exists')
            except result_model.DoesNotExist:
                print('SAVING profile')
                result_instance = result_model(**json.loads(self.raw_res))
                result_instance.mg_file = mg_file
                result_instance.save()
        # self.raw_res = '{}'
        # except:
        #     print('ERROR')
        # super().save(*args, **kwargs)


# class TmticResult(models.Model):

def fastqc_img_path(instance, filename):
    return '{df}/{preproc}/{sample}/{strand}/fastqc/{file}.png'.format(
        df=instance.mg_file.container.mg_sample.dataset_hard.df_name,
        preproc=instance.mg_file.container.preprocessing,
        sample=instance.mg_file.container.mg_sample.name_on_fs,
        strand=instance.mg_file.strand,
        file=filename)


class Mp2Result(models.Model):
    mg_container = models.ForeignKey(MgSampleFileContainer, on_delete=models.CASCADE)
    params = models.CharField(max_length=10)
    report = models.FileField(upload_to=None, blank=True, null=True)

    def __str__(self):
        return self.mg_container.mg_sample.name_on_fs + ' ' + self.mg_container.preprocessing + ' ' + self.params


class ProfileResult(models.Model):
    mg_file = models.ForeignKey(MgFile, on_delete=models.CASCADE, related_name='profile', unique=True)
    # general_result = models.ForeignKey(GeneralResult, on_delete=models.CASCADE)

    bp = models.IntegerField()
    reads = models.IntegerField()

    file_type = models.CharField(max_length=128)
    encoding = models.CharField(max_length=128)
    sequence_length = models.CharField(max_length=128)
    per_tile_sequence_quality = models.CharField(max_length=128, blank=True, null=True)
    basic_statistics = models.CharField(max_length=10)
    per_base_sequence_quality = models.CharField(max_length=10)
    per_sequence_quality_scores = models.CharField(max_length=10)
    per_base_sequence_content = models.CharField(max_length=10)
    per_sequence_gc_content = models.CharField(max_length=10)
    per_base_n_content = models.CharField(max_length=10)
    sequence_length_distribution = models.CharField(max_length=10)
    sequence_duplication_levels = models.CharField(max_length=10)
    overrepresented_sequences = models.CharField(max_length=10)
    adapter_content = models.CharField(max_length=10)
    sequences_flagged_as_poor_quality = models.IntegerField(max_length=10)

    adapter_content_img = models.ImageField(upload_to=None, blank=True, null=True)
    duplication_levels_img = models.ImageField(upload_to=None, blank=True, null=True)
    per_base_n_content_img = models.ImageField(upload_to=None, blank=True, null=True)
    per_base_quality_img = models.ImageField(upload_to=None, blank=True, null=True)
    per_base_sequence_content_img = models.ImageField(upload_to=None, blank=True, null=True)
    per_sequence_gc_content_img = models.ImageField(upload_to=None, blank=True, null=True)
    per_sequence_quality_img = models.ImageField(upload_to=None, blank=True, null=True)
    sequence_length_distribution_img = models.ImageField(upload_to=None, blank=True, null=True)


class TestResult(models.Model):
    name = models.CharField(max_length=128)
