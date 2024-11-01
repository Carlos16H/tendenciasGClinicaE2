from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import MedicalRMedicineI
from ..medicineInventory.models import MedicineInventory
from ..Billing.models import Billing
from ..TypeAppointment.models import TypeAppointment
from ..MedicalRecords.models import MedicalRecords

@receiver(pre_save, sender=MedicalRMedicineI)
def validate_quantity(sender, instance, **kwargs):
    
    medicine_inventory = MedicineInventory.objects.get(id=instance.idMedicineInventory_id)
    
    # Verifica si la cantidad disponible es suficiente
    if medicine_inventory.quantityAvailable < instance.amount:
        raise ValidationError("No hay inventario suficiente para realizar esta operación.")
    
    # Si es suficiente, reduce la cantidad disponible
    medicine_inventory.quantityAvailable -= instance.amount
    medicine_inventory.save()
    
@receiver(post_save, sender=MedicalRMedicineI)
def update_total_billing(sender, instance, **kwargs):
    matching_records = MedicalRMedicineI.objects.filter(idMedicalRecords_id=instance.idMedicalRecords_id)
    total_in_medicine = 0
    for record in matching_records:
        inventory_cost = MedicineInventory.objects.get(id=record.idMedicineInventory_id).cost
        total_cost = record.amount * inventory_cost
        total_in_medicine += total_cost

    billing_records = Billing.objects.filter(idMedicalRecords_id=instance.idMedicalRecords_id)
    for billing in billing_records:
        billing.totalAmount = TypeAppointment.objects.get(id=MedicalRecords.objects.get(
            id=billing.idMedicalRecords_id).idTypeAppointment_id
        ).cost + total_in_medicine
        billing.save()