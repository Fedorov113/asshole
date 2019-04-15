import json

from rest_framework import serializers
from explorer.models import *


class ResultTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultType
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['input_schema'] = json.loads(ret['input_schema'])
        return ret