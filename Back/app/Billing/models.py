from django.db import models
from ..MedicalRecords.models import MedicalRecords
from ..Patients.models import Patients

class Billing(models.Model):
    class Meta:
        verbose_name = "Billing"
        verbose_name_plural = "Billings"
    
    class PaymentStatus(models.TextChoices):
        PAG = "PAG", "Pagado"
        PEND = "PEND", "Pendiente"
        
    idPatients = models.ForeignKey(Patients, on_delete=models.CASCADE, blank=False)
    idMedicalRecords = models.ForeignKey(MedicalRecords, on_delete=models.CASCADE, blank=False)
    date = models.DateField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField('Details', max_length=100, blank = True)
    paymentStatus = models.CharField(
        'Estado de pago',
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PEND
    )
    
    
    def __str__(self):
        return f'{self.date} - {self.idPatients} - {self.idMedicalRecords} - {self.totalAmount}'