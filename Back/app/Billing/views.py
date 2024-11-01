from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Billing
from .serializers import BillingsSerializers
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class BillingsViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingsSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,  
        filters.OrderingFilter,
    ]
    
    filterset_fields = ('__all__')
    search_fields = ('idPatient__firstName', 'idMedicalRecords__description', 'date','paymentStatus')
    ordering_fields = ('__all__')


    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_billing_to_pdf(self, request, pk=None):
        billing = get_object_or_404(Billing, pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="billing_{billing.id}.pdf"'
        y = 670

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(f"Facturación {billing.idPatients.firstName} {billing.idPatients.lastName}")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Facturación/Copagos"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(100, 700, "DETALLES")
            
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(100, y, f"Paciente: {billing.idPatients.firstName} {billing.idPatients.lastName}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Profesional: {billing.idMedicalRecords.idEmployees.firstName} {billing.idMedicalRecords.idEmployees.lastName}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Tipo Cita: {billing.idMedicalRecords.idTypeAppointment.nameAppointment}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Descripción: {billing.idMedicalRecords.description}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Fecha Cita: {billing.idMedicalRecords.dateCreated.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Fecha Facturación: {billing.date}")  
        y -= 20
        pdf_canvas.drawString(100, y, f"Total: {billing.totalAmount}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Estado Pago: {billing.paymentStatus}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Detalles facturación: {billing.details}")
        y -= 20

        pdf_canvas.save()

        return response
    
    @action(detail=False, methods=['get'], url_path='export-all-pdf')
    def export_all_billings_to_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_billings.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle("Exporte Facturación/Copagos")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Facturación"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(100, 700, "INFORMACIÓN GENERAL FACTURACIÓN")

        pdf_canvas.setFont("Helvetica", 10)
        y = 670
        for billing in Billing.objects.all():
            if y < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 10)
                y = 750

            pdf_canvas.drawString(100, y, f"Paciente: {billing.idPatients.firstName} {billing.idPatients.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Profesional: {billing.idMedicalRecords.idEmployees.firstName} {billing.idMedicalRecords.idEmployees.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Tipo Cita: {billing.idMedicalRecords.idTypeAppointment.nameAppointment}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Descripción: {billing.idMedicalRecords.description}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Fecha Cita: {billing.idMedicalRecords.dateCreated.strftime('%Y-%m-%d %H:%M:%S')}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Fecha Facturación: {billing.date}")  
            y -= 20
            pdf_canvas.drawString(100, y, f"Total: {billing.totalAmount}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Estado Pago: {billing.paymentStatus}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Detalles facturación: {billing.details}")
            y -= 20
            pdf_canvas.drawString(100, y, f"------------------------------------------------------------------")
            y -= 30


        pdf_canvas.save()

        return response
