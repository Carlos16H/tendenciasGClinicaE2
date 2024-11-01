from rest_framework import serializers
from .models import Appointment
from ..Patients.models import Patients
from ..Employees.models import Employees


class AppointmentsSerializers(serializers.ModelSerializer):
    idEmployee = serializers.PrimaryKeyRelatedField(queryset=Employees.objects.all())
    idPatient = serializers.PrimaryKeyRelatedField(queryset=Patients.objects.all())
    
    class Meta:
        model = Appointment
        fields = ['id', 'idPatient', 'idEmployee', 'datetime', 'reason', 'status']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = {
            'id': instance.idEmployee.id,
            'firstName': instance.idEmployee.firstName,
            'lastName': instance.idEmployee.lastName,
            'email': instance.idEmployee.email,
        }
        representation['patient'] = {
            'id': instance.idPatient.id,
            'firstName': instance.idPatient.firstName,
            'lastName': instance.idPatient.lastName,
            'email': instance.idPatient.email,
        }
        return representation