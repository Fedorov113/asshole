from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()

class SampleFSSerializer(serializers.Serializer):
    sample_name = StringListField()
#
# class Mp2DataSerializer(serializers.Serializer):
#
#
#
