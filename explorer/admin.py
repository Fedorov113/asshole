from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Dataset)
admin.site.register(Subject)
admin.site.register(ActualShitSample)
admin.site.register(StoolMgSample)
admin.site.register(StoolMgSampleFileConatiner)
admin.site.register(StoolMgSampleFile)
admin.site.register(FMT)
