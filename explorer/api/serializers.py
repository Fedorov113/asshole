from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()

class SampleFSSerializer(serializers.Serializer):
    sample_name = StringListField()

class RefSeqSetsSerializer(serializers.Serializer):
    type = serializers.CharField()
    seqs = serializers.ListField(child = serializers.CharField())

