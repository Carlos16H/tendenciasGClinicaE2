from django.shortcuts import render
from rest_framework import viewsets
from .models import * 
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class MedicalRMedicineIViewSet(viewsets.ModelViewSet):
    queryset = MedicalRMedicineI.objects.all()
    serializer_class = MedicalRMedicineISerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,  
        filters.OrderingFilter,
    ]
    
    filterset_fields = ('__all__')
    search_fields = ('id', 'idMedicalRecords__idPatient', 'idMedicineInventory__nameMedicine')
    ordering_fields = ('__all__')
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)