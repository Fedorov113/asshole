from rest_framework import serializers
from explorer.models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        # fields = ('id', 'df_name')
        fields = '__all__'