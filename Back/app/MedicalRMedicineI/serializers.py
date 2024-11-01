from rest_framework import serializers

from app.TypeAppointment.serializers import TypeAppointmentSerializers
from ..MedicalRMedicineI.models import MedicalRMedicineI
from ..MedicalRecords.models import MedicalRecords
from ..medicineInventory.models import MedicineInventory
from ..TypeAppointment.models import TypeAppointment
import json

class MedicalRMedicineISerializers(serializers.ModelSerializer):
    idMedicalRecords = serializers.PrimaryKeyRelatedField(queryset=MedicalRecords.objects.all())
    idMedicineInventory = serializers.PrimaryKeyRelatedField(queryset=MedicineInventory.objects.all())
    
    class Meta:
        model = MedicalRMedicineI
        fields = ('__all__')
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        obj = TypeAppointmentSerializers(TypeAppointment.objects.get(id = instance.idMedicalRecords.idTypeAppointment_id)).data
        representation['medicalRecords'] = {
            'id': instance.idMedicalRecords.id,
            'typeAppointment': obj,

        }
        representation['medicineInventory'] = {
            'id': instance.idMedicineInventory.id,
            'nameMedicine': instance.idMedicineInventory.nameMedicine,
            'description': instance.idMedicineInventory.description,
            'quantityAvailable': instance.idMedicineInventory.quantityAvailable,
            'cost': instance.idMedicineInventory.cost
        }
        return representation