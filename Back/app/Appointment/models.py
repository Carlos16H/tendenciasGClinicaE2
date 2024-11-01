from django.db import models
from ..Employees.models import Employees
from ..Patients.models import Patients

class Appointment(models.Model):
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
    
    class AppointmentStatus(models.TextChoices):
        PROGR = "PROGR", "Programada"
        COMPL = "COMPL", "Completada"
        CANCEL = "CANCEL", "Cancelada"

    idPatient = models.ForeignKey(Patients, on_delete=models.CASCADE, blank=False)
    idEmployee = models.ForeignKey(Employees, on_delete=models.CASCADE, blank=False)
    datetime = models.DateTimeField(blank=False, null=False)
    reason = models.CharField('Reason', max_length=100, blank=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PROGR
    )
    
    def __str__(self):
        return f'{self.datetime} - {self.idPatient} - {self.idEmployee} - {self.reason}'