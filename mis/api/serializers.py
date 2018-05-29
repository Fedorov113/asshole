from rest_framework import serializers
from mis.models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'pk',
            'person_name',
            'date_of_birth',
            'gender',
            'diagnosis',
            'notes'
        ]