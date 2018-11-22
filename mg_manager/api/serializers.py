from rest_framework import serializers

from explorer.file_system.file_system_helpers import import_sample
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



class SampleSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleSource
        fields = '__all__'


class RealSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealSample
        fields = '__all__'

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class MgFileSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField( required=False, queryset=MgSampleFileContainer.objects.all())
    profile = ProfileResultSerializer(many=True, required=False)
    class Meta:
        model = MgFile
        fields = '__all__'
        extra_fields = ['profile']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MgFileSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

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
    df = serializers.PrimaryKeyRelatedField(required=False, queryset=DatasetHard.objects.all())
    containers = MgSampleFileContainerSerializer(many=True)

    class Meta:
        model = MgSample
        fields = '__all__'
        extra_fields = ['containers']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MgSampleSerializer, self).get_field_names(declared_fields, info)
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
                        new_file = MgFile.objects.create(container=cont, **file_data)

                        data = {
                            'orig_file': new_file.orig_file_location,
                            'df': mg_sample.dataset_hard.df_name,
                            'strand':new_file.strand,
                            'sample': mg_sample.name_on_fs
                        }

                        print(data)

                        imp = import_sample(data)
                        if imp:
                            new_file.import_success = True
                            new_file.save()
            return mg_sample
        else:
            return MgSample.objects.create(**validated_data)


class DatasetHardFullSerializer(serializers.ModelSerializer):

    samples = MgSampleSerializer(many=True)

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
