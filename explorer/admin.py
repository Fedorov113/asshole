from django.contrib import admin

# Register your models here.

from .models import Dataset
from .models import Sample


admin.site.register(Dataset)
admin.site.register(Sample)
