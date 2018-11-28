from django.db import models


class DatasetHard(models.Model):
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')
    comes_from = models.CharField(max_length=256, default='Internal')

    def __str__(self):
        return self.df_name



class SampleSource(models.Model):
    source_name = models.CharField(max_length=200, unique=True)
    source_description = models.TextField()
    df = models.ForeignKey(DatasetHard, on_delete=models.CASCADE)

    def __str__(self):
        return self.source_name

class RealSample(models.Model):
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE)
    date_of_collection = models.DateField()
    serial_number = models.PositiveIntegerField()
    name = models.CharField(max_length=200, blank=True)
    # SHOULD BE JSON
    meta_info = models.TextField(blank=True)

    class Meta:
        unique_together = ('source', 'serial_number')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.source.source_name + 'T' + str(self.serial_number)
        super(RealSample, self).save(*args, **kwargs)


class Library(models.Model):
    library_name = models.CharField(max_length=200, unique=True)
    date_of_preparation = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.library_name


class LibrarySample(models.Model):
    real_sample = models.ForeignKey(RealSample, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.real_sample.name + '_L' + str(self.library.pk)
        super(LibrarySample, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# PROTOCOL
class SequencingRun(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=32, unique=True)
    platform = models.CharField(max_length=200)
    date_of_run = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.platform


class MgSample(models.Model):
    name = models.CharField(max_length=200, blank=True)
    # TODO rework unique
    name_on_fs = models.CharField(max_length=200, blank=True, unique=True)
    uuid_from_km = models.CharField(max_length=256, blank=True, null=True)

    library_sample = models.ForeignKey(LibrarySample, on_delete=models.CASCADE, blank=True, null=True)
    sequencing_run = models.ForeignKey(SequencingRun, on_delete=models.CASCADE, blank=True, null=True)

    dataset_hard = models.ForeignKey(DatasetHard, on_delete=models.CASCADE, related_name='samples')
 
    def save(self, *args, **kwargs):
        if self.library_sample is not None and self.sequencing_run is not None:
            self.name = self.library_sample.name + '_B' + str(self.sequencing_run.pk)
        super(MgSample, self).save(*args, **kwargs)

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