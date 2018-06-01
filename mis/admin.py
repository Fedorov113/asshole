from django.contrib import admin

# Register your models here
from .models import *

admin.site.register(DiseaseTerminology)
admin.site.register(Person)
admin.site.register(GeneralObservation)
admin.site.register(StoolSample)