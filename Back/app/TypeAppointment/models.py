from django.db import models

# Create your models here.
class TypeAppointment(models.Model):
    
    class Meta:
        verbose_name = "TypeAppointment"
        verbose_name_plural = "TypeAppointment"
    
    
    nameAppointment = models.CharField('Nombre cita', max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=0)
    
    def __str__(self):
        return f'{self.nameAppointment}- {self.cost}'