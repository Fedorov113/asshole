from rest_framework import serializers
from explorer.models import Dataset

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