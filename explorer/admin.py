from django.contrib import admin

from .models import *

admin.site.register(SnakeRuleResult)
admin.site.register(SnakeRule)
admin.site.register(Parameter)
admin.site.register(Tool)
admin.site.register(Result)
admin.site.register(ResultTypes)



