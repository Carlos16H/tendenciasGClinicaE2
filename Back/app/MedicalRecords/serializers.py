from rest_framework import serializers
from .models import MedicalRecords
from ..Employees.models import Employees
from ..Patients.models import Patients
from ..TypeAppointment.models import TypeAppointment

class MedicalRecordSerializers(serializers.ModelSerializer):
    # Este campo permite aceptar el ID del empleado al crear o actualizar
    idEmployees = serializers.PrimaryKeyRelatedField(queryset=Employees.objects.all())
    idPatient = serializers.PrimaryKeyRelatedField(queryset=Patients.objects.all())
    idTypeAppointment = serializers.PrimaryKeyRelatedField(queryset=TypeAppointment.objects.all())

    class Meta:
        model = MedicalRecords
        fields = ['id', 'idPatient', 'description', 'idEmployees', 'dateCreated', 'idTypeAppointment']

    def to_representation(self, instance):
        # Representación personalizada para incluir id, nombre y email del empleado en 'idEmployees'
        representation = super().to_representation(instance)
        representation['employee'] = {
            'id': instance.idEmployees.id,
            'firstName': instance.idEmployees.firstName,
            'lastName': instance.idEmployees.lastName,
            'email': instance.idEmployees.email,
        }
        representation['patient'] = {
            'id': instance.idPatient.id, 
            'firstName': instance.idPatient.firstName,
            'lastName': instance.idPatient.lastName,
        }
        representation['typeAppointment'] = {
            'id': instance.idTypeAppointment.id,
            'nameAppointment': instance.idTypeAppointment.nameAppointment,
            'cost': instance.idTypeAppointment.cost,
        }
        return representation