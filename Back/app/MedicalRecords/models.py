from django.db import models
from ..Patients.models import Patients
from ..Employees.models import Employees
from ..TypeAppointment.models import TypeAppointment
from django.utils import timezone

class MedicalRecords(models.Model):
    class Meta:
        verbose_name = "MedicalRecord"
        verbose_name_plural = "MedicalRecords"
        
    idPatient = models.ForeignKey(Patients, on_delete=models.CASCADE, blank=False)
    description = models.TextField('Description', max_length=100, blank = True)
    idEmployees = models.ForeignKey(Employees, on_delete=models.CASCADE, blank=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    idTypeAppointment = models.ForeignKey(TypeAppointment, on_delete=models.CASCADE, blank=False)
    
    
    def __str__(self):
        return f'{self.idPatient} - {self.description}'