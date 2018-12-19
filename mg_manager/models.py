from django.db import models

class MetaSchema(models.Model):
    name = models.CharField(max_length=200, unique=True)
    schema = models.TextField(blank=True)  # FLAT JSON

    def __str__(self):
        return self.name

class DatasetHard(models.Model):
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')
    comes_from = models.CharField(max_length=256, default='Internal')

    def __str__(self):
        return self.df_name


class SampleSource(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    meta_schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE, blank=True, null=True)

    meta_info = models.TextField(blank=True)  # FLAT JSON
    ids = models.TextField(blank=True)  # {'service': <identificator>}; {'rcpcm_cdr': 1234dcertr}

    def __str__(self):
        return self.name


class RealSample(models.Model):
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE, related_name='real_samples')
    description = models.TextField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    date_of_collection = models.DateField(blank=True, null=True)
    time_point = models.PositiveIntegerField(blank=True, null=True)
    meta_schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = models.TextField(blank=True)  # FLAT JSON
    class Meta:
        unique_together = ('source', 'name')

    def __str__(self):
        return self.source.name + '_' + self.name


class Library(models.Model):
    library_name = models.CharField(max_length=200, unique=True)
    date_of_preparation = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.library_name


class SequencingRun(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=32, unique=True)
    platform = models.CharField(max_length=200)
    date_of_run = models.DateField()
    description = models.TextField()



    def __str__(self):
        return self.name + ' ' + self.platform


class MgSample(models.Model):
    dataset_hard = models.ForeignKey(DatasetHard, on_delete=models.CASCADE, related_name='samples')
    real_sample = models.ForeignKey(RealSample, on_delete=models.CASCADE, blank=True, null=True,  related_name='mg_samples')
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=200, blank=True)
    name_on_fs = models.CharField(max_length=200, blank=True)

    library = models.ForeignKey(Library, on_delete=models.CASCADE, blank=True, null=True)
    sequencing_run = models.ForeignKey(SequencingRun, on_delete=models.CASCADE, blank=True, null=True)



    class Meta:
        unique_together = ('dataset_hard', 'name_on_fs', 'library', 'sequencing_run')

    def __str__(self):
        return self.name


class MgSampleFileContainer(models.Model):
    mg_sample = models.ForeignKey(MgSample, related_name='containers', on_delete=models.CASCADE)

    preprocessing = models.CharField(max_length=512)

    def __str__(self):
        return self.mg_sample.name + ' ' + self.preprocessing


def sample_file_path(instance, filename):
    return '{df}/{preproc}/{sample}/{strand}/fastqc/{file}.png'.format(
        df=instance.container.mg_sample.dataset_hard.df_name,
        preproc=instance.container.preprocessing,
        sample=instance.container.mg_sample.name_on_fs,
        strand=instance.strand,
        file=filename)


class MgFile(models.Model):
    container = models.ForeignKey(MgSampleFileContainer, related_name='files', on_delete=models.CASCADE)

    R1 = 'R1'
    R2 = 'R2'
    S = 'S'

    STRAND_CHOICES = (
        (R1, 'R1'),
        (R2, 'R2'),
        (S, 'S')
    )

    strand = models.CharField(max_length=3, choices=STRAND_CHOICES, default=S)

    # NOT BLANK IF IT IS IMPORTED FROM SOMEWHERE
    orig_file_location = models.CharField(max_length=1024, blank=True)
    import_success = models.BooleanField(default=False)

    def __str__(self):
        return self.container.__str__() + ' ' + self.strand


class DatasetSoft(models.Model):
    name = models.CharField(max_length=256, unique=True)
    df_description = models.CharField(max_length=1024, default='Empty')
    dataset_soft = models.ManyToManyField(MgSample, blank=True)

    def __str__(self):
        return self.name
