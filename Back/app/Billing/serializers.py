from rest_framework import serializers
from .models import Billing
from ..Patients.models import Patients
from ..MedicalRecords.models import MedicalRecords

class BillingsSerializers(serializers.ModelSerializer):
    idPatients = serializers.PrimaryKeyRelatedField(queryset=Patients.objects.all())
    idMedicalRecords = serializers.PrimaryKeyRelatedField(queryset=MedicalRecords.objects.all())
    
    class Meta:
        model = Billing
        fields = ('__all__')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = {
            'id': instance.idPatients.id,
            'firstName': instance.idPatients.firstName,
            'lastName': instance.idPatients.lastName,
            'Cedula': instance.idPatients.Cedula,
        }
        representation['medicalRecords'] = {
            'id': instance.idMedicalRecords.id,
            'description': instance.idMedicalRecords.description,
            'dateCreated': instance.idMedicalRecords.dateCreated,
            'nameAppointment': instance.idMedicalRecords.idTypeAppointment.nameAppointment,
        }
        return representation