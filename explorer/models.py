from django.db import models
from mis.models import StoolSample

class Dataset(models.Model):
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')
    def __str__(self):
        return self.df_name

class Sample(models.Model):

    stool_sample = models.ForeignKey(StoolSample, on_delete=models.CASCADE)
    sample_name_to_use_in_pipeline = models.CharField(max_length=200, unique=True)

    # Needed for better managing newly added files
    was_processed = models.BooleanField()
    final_ready = models.BooleanField()

    def __str__(self):
        return self.sample_name_to_use_in_pipeline





#
# class File(models.Model):
#
#     Sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=200, unique=True)
#
#     def __str__(self):
#         return self.file_name
#
