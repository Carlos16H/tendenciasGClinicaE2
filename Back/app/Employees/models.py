from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.

class EmployeesManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Esto encripta la contraseña automáticamente
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class Employees(AbstractBaseUser, PermissionsMixin):
    
    class Meta:
        verbose_name = "Employees"
        verbose_name_plural = "Employees"
        
    firstName = models.CharField('Nombres', max_length=100)
    lastName = models.CharField('Apellidos', max_length=100)
    email = models.EmailField('Correo electrónico', max_length=100)
    phone = models.CharField('Celular', max_length=10)
    birthdate = models.DateField('Fecha de nacimiento', blank=True, null=True)
    address = models.CharField('Dirección', max_length=100)
    rol_options = (
        ("MED", "Medico(a)"),
        ("ENF", "Enfermero(a)"),
        ("ADM", "Administrativo"),
        ("LIM", "Limpieza"),
        ("REG", "Regente de farmacia"),
        ("FIS", "Fisioterapeuta"),
        ("OTR", "Otros")
    )
    
    rol = models.CharField('Cargo', max_length=50, blank=False, null=False, choices=rol_options, default='OTR')
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = EmployeesManager()

    USERNAME_FIELD = 'username'  # Campo que será usado como nombre de usuario
    REQUIRED_FIELDS = ['email', 'firstName', 'lastName', 'phone', 'birthdate', 'address', 'rol']
    
    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.rol} - {self.username}"