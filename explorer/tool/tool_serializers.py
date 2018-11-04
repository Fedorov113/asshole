from rest_framework import serializers
from explorer.models import *
from django.conf import settings

import requests
import json

class ParamsSerializer(serializers.ModelSerializer):
    tool = serializers.PrimaryKeyRelatedField(required=False, queryset=Tool.objects.all())

    class Meta:
        model = Parameter
        fields = '__all__'

# loads all info about parameters
class ToolSerializerFull(serializers.ModelSerializer):

    parameters = ParamsSerializer(many=True)

    class Meta:
        model = Tool
        fields = '__all__'
        extra_fields = ['parameters']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ToolSerializerFull, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields