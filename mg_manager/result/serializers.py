from rest_framework import serializers
from .models import ProfileResult
from ..models import MgFile

class ProfileResultSerializer(serializers.ModelSerializer):
    file = serializers.PrimaryKeyRelatedField( required=False, queryset=MgFile.objects.all())

    class Meta:
        model = ProfileResult
        fields = ['id','file', 'bp', 'reads']
        # fields = '__all__'
        #

class ProfileResultFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileResult
        fields = '__all__'
        # fields = '__all__'