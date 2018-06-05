from rest_framework import serializers
from explorer.models import *

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'pk',
            'df_name',
            'df_description'
        ]
    # coverts to JSON
    # validation for data passed

    def validate_df_name(self, value):
        qs = Dataset.objects.filter(df_name__iexact=value)
        if self.instance:
            qs =qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The Dataset name must be unique")
        return value

class FmtSerializer(serializers.ModelSerializer):
    class Meta:
        model = FMT
        fields = (
            'donor_actual_shit',
            'recipient',
            'date_of_fmt',
            'type'
        )

class ActualShitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualShitSample
        fields = (
            'pk',
            'stool_sample',
            'subject',
            'subject_nickname',
            'date_of_collection',
            'clinical_index_value',
            'clinical_index_name',
            'point_referent_to_fmt'
        )

    subject_nickname = serializers.SerializerMethodField()
    def get_subject_nickname(self, obj):
        return obj.subject.subject_nickname

class SubjectSerializer(serializers.ModelSerializer):
    # shit_samples=serializers.StringRelatedField(many=True)
    shit_samples = ActualShitSerializer(many=True, read_only=True)
    class Meta:
        model = Subject
        fields = (
            'pk',
            'subject_nickname',
            'gender',
            'diagnosis_term',
            'diagnosis_name_in_study',
            'age',
            'additional_info',
            'shit_samples'
        )

