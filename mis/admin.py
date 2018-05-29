from django.contrib import admin

# Register your models here.
from .models import Person
from .models import FMT
from .models import GeneralObservation
from .models import StoolSample

admin.site.register(Person)
admin.site.register(FMT)
admin.site.register(GeneralObservation)
admin.site.register(StoolSample)