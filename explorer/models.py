from django.db import models

# Create your models here.

class Dataset(models.Model):
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')
    def __str__(self):
        return self.df_name

class Person(models.Model):
    #Person comes from study?

    # General Info
    person_name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField('Birth Date', auto_now=True)
    gender = models.CharField(max_length=200)

    # Health related
    diagnosis = models.CharField(max_length=200)
    additional_health_info = models.CharField(max_length=2000)
    therapy = models.CharField(max_length=2000)

    # Misc
    notes = models.CharField(max_length=2000)


    def __str__(self):
        return self.person_name
#
# class Observation(models.Model):
#
#
#     subject
#     doctor
#     hospital
#     date_of_observation


# class Therapy(models.Model):


# class Episode(models.Model):




class Batch(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.batch_name

class Sample(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    date_of_collection = models.DateTimeField('When sample was collected', auto_now=True)
    date_of_preproc = models.DateTimeField('When sample was preprocessed', auto_now=True)
    sample_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.sample_name

class File(models.Model):
    Sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.file_name

