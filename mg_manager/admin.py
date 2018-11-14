from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DatasetHard)
admin.site.register(DatasetSoft)

admin.site.register(SampleSource)
admin.site.register(RealSample)

admin.site.register(Library)
admin.site.register(LibrarySample)

admin.site.register(SequencingRun)
admin.site.register(MgSample)
admin.site.register(MgSampleFileContainer)
admin.site.register(MgFile)
