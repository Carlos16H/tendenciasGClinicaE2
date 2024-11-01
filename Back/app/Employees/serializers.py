from rest_framework import serializers
from .models import Employees
from django.contrib.auth.hashers import make_password
from django.contrib.auth import hashers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class EmployeesSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) #No permite leer la contraseña
        
    class Meta:
        model = Employees
        fields = ('__all__')
        

    def create (self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Employees.objects.create(**validated_data)
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        
    def validate(self, attrs):
        # Se usa el nombre de usuario y contraseña proporcionados para autenticación
        username = attrs.get("username")
        password = attrs.get("password")

        # Se intenta autenticar el usuario
        user = authenticate(username=username, password=password)

        if user is not None:
            
            """ if user.rol != 'ADM':
                raise serializers.ValidationError({
                    "detail": "No tienes permisos para acceder."
                }) """
            # Si el usuario se autentica correctamente, se continúa con la generación del token
            data = super().validate(attrs)
            
            data['firstName'] = self.user.firstName
            data['lastName'] = self.user.lastName
            data['email'] = self.user.email
            data['rol'] = self.user.rol
            return data
        else:
            # Si la autenticación falla, se genera un error personalizado
            raise serializers.ValidationError({
                "detail": "Credenciales incorrectas, por favor verifica tu usuario o contraseña."
            })