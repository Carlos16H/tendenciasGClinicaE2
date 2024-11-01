from rest_framework import serializers
from .models import Patients
from django.contrib.auth.hashers import make_password
from django.contrib.auth import hashers

class PatientsSerializers(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Patients
        fields = ('__all__')
        
    """ def create(self, validated_data):
        user = Patients.objects.create(
            username = validated_data['username'],
            password = make_password(validated_data['password'])
        )
        return user """
    
    """ def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Patients.objects.create(**validated_data) """