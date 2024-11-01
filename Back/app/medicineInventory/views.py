from django.http import HttpResponse
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import * 
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class medicineInventoryViewset(viewsets.ModelViewSet):
    queryset = MedicineInventory.objects.all()
    serializer_class = medicineInventorySerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    filterset_fields = ('__all__')
    search_fields = ('nameMedicine', 'description', 'quantityAvailable')
    ordering_fields = ('__all__')

    #permission_classes = [AllowAny]


    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_medicine_to_pdf(self, request, pk=None):
        medicine = get_object_or_404(MedicineInventory, pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="medicine_{medicine.id}.pdf"'
        
        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(f"Inventario Medicamento: {medicine.nameMedicine}")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Detalles del Medicamento"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(100, 700, "DETALLES DEL MEDICAMENTO")
        
        pdf_canvas.setFont("Helvetica", 10)
        y = 670
        pdf_canvas.drawString(100, y, f"Nombre: {medicine.nameMedicine}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Descripción: {medicine.description}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Cantidad Disponible: {medicine.quantityAvailable}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Precio Unitario: {medicine.cost}")
        y -= 20

        pdf_canvas.save()
        return response

    @action(detail=False, methods=['get'], url_path='export-all-pdf')
    def export_all_medicines_to_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_medicines.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle("Inventario Completo de Medicamentos")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Inventario de Medicamentos"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(100, 700, "INFORMACIÓN DEL INVENTARIO")

        pdf_canvas.setFont("Helvetica", 10)
        y = 670
        for medicine in MedicineInventory.objects.all():
            if y < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 10)
                y = 750

            pdf_canvas.drawString(100, y, f"Nombre: {medicine.nameMedicine}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Descripción: {medicine.description}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Cantidad Disponible: {medicine.quantityAvailable}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Precio Unitario: {medicine.cost}")
            y -= 30
            pdf_canvas.drawString(100, y, f"--------------------------------------------")
            y -= 30

        pdf_canvas.save()
        return response