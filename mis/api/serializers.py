from rest_framework import serializers
from mis.models import Person

class PersonSerializer(serializers.ModelSerializer):
    diagnosis = serializers.CharField(source='get_diagnosis_display')
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Person
        fields = [
            'pk',
            'person_name',
            'person_nickname',
            'date_of_birth',
            'gender',
            'diagnosis',
            'notes'
        ]