from django.db import models
from mis.models import Person
import mis

class Dataset(models.Model):
    df_name = models.CharField(max_length=200, unique=True)
    comes_from = models.CharField(max_length=100)
    df_description = models.CharField(max_length=2000, default='Empty')
    def __str__(self):
        return self.df_name

class Subject(models.Model):
    # dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    # ANON. Should be unique
    subject_nickname = models.CharField(max_length=200, unique=True)
    # This reference to person in EHR, can be empty, if data comes not from EHR
    # Good comment on blank and null
    # stackoverflow.com/questions/16589069/foreignkey-does-not-allow-null-values
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    # Obviously, gender
    gender = models.CharField(max_length=100, choices=Person.GenderChoice)
    # Hmm, how to map it easily?
    # We should bind to terminology obviously
    # But different names can be used in studies
    diagnosis_term = models.ForeignKey(mis.models.DiseaseTerminology, on_delete=models.CASCADE)
    # So create another field!
    diagnosis_name_in_study = models.CharField(max_length=100)
    # Should we use just a number, which is easier to implement or date?
    # Both, if we have access?
    # Let's start with:
    age = models.IntegerField()
    # JSON field with additional info
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject_nickname


# The reason we use metagenomic sample is that one physical sample can be sequenced a couple of times
# It can be preprocessed in different ways..
# TODO physical sample, library, mgSample...
class ActualShitSample(models.Model):
    # If we have access to EHR
    stool_sample = models.ForeignKey(mis.models.StoolSample, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject,related_name='shit_samples', on_delete=models.CASCADE)

    date_of_collection = models.DateField()
    # Clinical index at this observation point
    clinical_index_value = models.IntegerField()
    clinical_index_name = models.CharField(max_length=200)

    # 0 - before FMT. This is always 0 for donors
    point_referent_to_fmt = models.IntegerField()
    def __str__(self):
        return self.subject.subject_nickname +'_'+str(self.point_referent_to_fmt) \
               + ' at ' + str(self.date_of_collection)


class StoolMgSample(models.Model):
    # Link to Actual Shit!!
    actual_shit_sample = models.ForeignKey(ActualShitSample, on_delete=models.CASCADE)
    # Constructed as? What if we will combine different samples?
    sample_name_to_use_in_pipeline = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.sample_name_to_use_in_pipeline

class StoolMgSampleFileConatiner(models.Model):
    # Link all to info about mg sample
    stool_mg_sample = models.ForeignKey(StoolMgSample, on_delete=models.CASCADE)

    number_of_reads = models.IntegerField()
    mean_len_of_read = models.IntegerField()
    total_depth_in_bp = models.IntegerField()

    # Prepossessing string in prerpc_1__preproc2__ format
    # Reserved values: raw, final
    preproc = models.CharField(max_length=200)
    # JSON field with meatdata about preproc
    # or just params?
    # what if different types for strands?
    preproc_meta = models.TextField()

class StoolMgSampleFile(models.Model):
    stool_mg_sample_file_container = models.ForeignKey(StoolMgSampleFileConatiner, on_delete=models.CASCADE)

    location_on_disk = models.TextField()

    number_of_reads = models.IntegerField()
    mean_len_of_read = models.IntegerField()
    total_depth_in_bp = models.IntegerField()

class FMT(models.Model):
    donor_actual_shit = models.ForeignKey(ActualShitSample, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_of_fmt = models.DateField()
    type = models.CharField(max_length=200)

    def __str__(self):
        return str(self.recipient) + ' got ' + str(self.donor_actual_shit)