import json

import requests
from rest_framework import serializers

from asshole import settings
from explorer.file_system.file_system_helpers import import_sample_file
from ..models import *
from ..result.serializers import ProfileResultSerializer


class DatasetHardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetHard
        fields = '__all__'

    def validate_df_name(self, value):
        qs = DatasetHard.objects.filter(df_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The Dataset name must be unique")
        return value


class RealSampleIdSerializer(serializers.ModelSerializer):
    # source = serializers.PrimaryKeyRelatedField(required=False, queryset=SampleSource.objects.all())

    class Meta:
        model = RealSample
        fields = ['pk']


class SampleSourceSerializer(serializers.ModelSerializer):
    real_samples = RealSampleIdSerializer(many=True)

    class Meta:
        model = SampleSource
        fields = '__all__'
        extra_fields = ['real_samples']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(SampleSourceSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class SequencingRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRun
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class MgFileSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField(required=False, queryset=MgSampleFileContainer.objects.all())
    profile = ProfileResultSerializer(many=True, required=False)

    class Meta:
        model = MgFile
        fields = ['id', 'container', 'strand', 'profile', 'orig_file_location']


class MgSampleContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MgSampleFileContainer
        fields = '__all__'


class MgSampleContainerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MgFile
        fields = ['id', 'strand', 'container']


class MgSampleFileContainerSerializer(serializers.ModelSerializer):
    files = MgFileSerializer(many=True)
    mg_sample = serializers.PrimaryKeyRelatedField(required=False, queryset=MgSample.objects.all())

    class Meta:
        model = MgSampleFileContainer
        # fields = ['files', 'preprocessing']
        fields = '__all__'
        extra_fields = ['files']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MgSampleFileContainerSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class MgSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MgSample
        fields = '__all__'


class MgSampleFullSerializer(serializers.ModelSerializer):
    df = serializers.PrimaryKeyRelatedField(required=False, queryset=DatasetHard.objects.all())
    containers = MgSampleFileContainerSerializer(many=True)

    class Meta:
        model = MgSample
        fields = '__all__'
        extra_fields = ['containers']

    def get_field_names(self, declared_fields, info):
        print('getting field names')
        expanded_fields = super(MgSampleFullSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def create(self, validated_data):
        print('creating')

        if 'containers' in validated_data.keys():
            containers_data = validated_data.pop('containers')
            mg_sample = MgSample.objects.create(**validated_data)

            for container_data in containers_data:
                if 'files' in container_data.keys():
                    files_data = container_data.pop('files')
                    cont = MgSampleFileContainer.objects.create(mg_sample=mg_sample, **container_data)
                    for file_data in files_data:
                        new_file = MgFile(container=cont, **file_data)

                        data = {
                            'orig_file': new_file.orig_file_location,
                            'df': mg_sample.dataset_hard.df_name,
                            'strand': new_file.strand,
                            'sample': mg_sample.name_on_fs
                        }
                        url = settings.ASSHOLE_URL + 'api/fs/sample/import/'
                        r = requests.post(url, data=json.dumps(data))

                        if r.status_code == 201:
                            new_file.import_success = True
                            new_file.save()
            return mg_sample
        else:
            return MgSample.objects.create(**validated_data)


class DatasetHardFullSerializer(serializers.ModelSerializer):
    samples = MgSampleFullSerializer(many=True)

    class Meta:
        model = DatasetHard
        fields = '__all__'
        extra_fields = ['samples']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(DatasetHardFullSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
