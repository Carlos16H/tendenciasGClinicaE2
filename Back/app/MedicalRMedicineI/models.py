from django.db import models
from ..MedicalRecords.models import MedicalRecords
from ..medicineInventory.models import MedicineInventory

# Create your models here.

class MedicalRMedicineI(models.Model):
    class Meta:
        verbose_name = "MedicalRMedicineI"
        verbose_name_plural = "MedicalRMedicineI"
    
    
    idMedicalRecords = models.ForeignKey(MedicalRecords, on_delete=models.CASCADE, blank=False)
    idMedicineInventory = models.ForeignKey(MedicineInventory, on_delete=models.CASCADE, blank=False)
    amount = models.IntegerField('Cantidad')
    
    def __str__(self):
        return f'{self.idMedicalRecords} - {self.idMedicineInventory} - {self.amount}'