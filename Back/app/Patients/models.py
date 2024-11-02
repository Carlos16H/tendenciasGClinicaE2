from django.db import models

class Patients(models.Model):
    class Meta:
        verbose_name = "Patients"
        verbose_name_plural = "Patients"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEM = "F", "Female"
        OTHER = "O", "Other"

    firstName = models.CharField('First Name', max_length=100)
    lastName = models.CharField('Last name', max_length=100)
    email = models.CharField('Email', max_length=100)
    phone = models.CharField('Phone', max_length=10)
    birthDate = models.DateField('Birth Date', blank=False, null=False)
    address = models.CharField('Address', max_length=50)

    gender = models.CharField(
        'Gender',
        max_length=2,
        choices=Gender.choices,
        default=Gender.MALE
    )

    emergency_contact = models.CharField('Emergency Contact', max_length=50)
    emergency_contact_phone = models.CharField("Emergency Contact Phone", max_length=20, default='000-000-0000')
    insurance_entity = models.CharField("Insurance", max_length=50)
    policy_number = models.CharField("Insurance Number", max_length=20, default='0000000000')
    Policy_state = models.BooleanField("Valid Policy?", default=False)
    policy_validity = models.DateField('Insurance Active Until', blank=False, null=False, default='2000-01-01')
    Cedula = models.CharField('ID', max_length=10, default='0000000000')
    
    
    def __str__(self):
        return f'{self.firstName} - {self.email} - {self.phone}'