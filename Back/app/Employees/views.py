from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class EmployeesViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    filterset_fields = {
        'rol': ['exact', 'in'],  # Permite filtrar por rol específico o por múltiples valores
        'firstName': ['exact', 'icontains'],
        'lastName': ['exact', 'icontains'],
        'email': ['exact', 'icontains'],
        'phone': ['exact'],
        'birthdate': ['exact'],
        'address': ['exact', 'icontains'],
        'username': ['exact', 'icontains'],
    }
    search_fields = ('firstName', 'lastName', 'email', 'phone', 'birthdate', 'address', 'rol', 'username')
    ordering_fields = ('__all__')
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer