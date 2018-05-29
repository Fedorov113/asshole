from django.db import models
from enum import Enum


#
# class PainChoice(Enum):
#     NO = "No pain"
#     MIN = "Minimum pain"
#     MED = "Medium pain"
#     ST = "Severe pain"
#
# class YesNoChoice(Enum):
#     YES = "Yes"
#     NO = "No"
#
# class AppetiteChoice(Enum):
#     NO = "No appetite at all"
#     LOW = "Lowered appetite"
#     NORMAL = "Normal appetite"


#### DEMOGRAPHICS
class Person(models.Model):
    """
    Generic class for Person. Should be extended.
    """
    M = 'M'
    F = 'F'
    O = 'O'
    GenderChoice = (
        (M,"Male"),
        (F ,"Female"),
        (O , "Other")
    )

    BK = 'BK'
    YAK= 'YAK'
    SRK = 'SRK'
    H = 'H'
    DiagnosisChoice = (
        (BK, "Болезнь Крона"),
        (YAK, "Язвенный Колит"),
        (SRK, "Синдром Раздраженного Кишечника"),
        (H, "Здоров"),
    )

    # General Info
    person_name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField('Birth Date')
    gender = models.CharField(max_length=100, choices=GenderChoice)
    diagnosis = models.CharField(max_length=100, choices=DiagnosisChoice, default=H)

    # Misc
    notes = models.CharField(max_length=2000,null=True, blank=True)

    def __str__(self):
        return self.person_name


#### EHR
class StoolSample(models.Model):
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)

    where_obtained = models.CharField(max_length=200)
    where_now = models.CharField(max_length=200)

    # This nickname will be used along the life of sample. Must be unique.
    sample_nickname = models.CharField(max_length=200, unique=True)
    # Location of raw reads
    sample_location_on_fs = models.CharField(max_length=1000)

    date_of_collection = models.DateTimeField('When sample was collected')
    date_of_preproc = models.DateTimeField('When sample was preprocessed')
    date_of_sequencing = models.DateTimeField('When sample was sequenced')
    def __str__(self):
        return self.sample_nickname

class GeneralObservation(models.Model):
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    body_temperature = models.FloatField(default=36.6)
    stool_per_day = models.IntegerField(default=1)
    sludge_in_stool = models.IntegerField(default=0)
    blood_in_stool = models.CharField(max_length=200)
    date_of_observation = models.DateTimeField('Date of observation')


class Therapy(models.Model):
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)

class FMT(models.Model):
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    transplant_sample = models.ForeignKey(StoolSample, on_delete=models.CASCADE)
    date_of_fmt = models.DateTimeField('When FMT was performed')

    def __str__(self):
        return self.transplant_sample.sample_nickname + '__to__' + self.patient.person_name
