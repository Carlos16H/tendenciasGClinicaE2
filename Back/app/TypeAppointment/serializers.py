from rest_framework import serializers
from .models import *

class TypeAppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = TypeAppointment
        fields = '__all__'