from django.http import HttpResponse
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from .models import MedicalRecords
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MedicalRecordSerializers
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecords.objects.all()
    serializer_class = MedicalRecordSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,  
        filters.OrderingFilter,
    ]
    
    filterset_fields = ('__all__')
    search_fields = ('id', 'idPatient__firstName', 'idEmployees__firstName', 'idTypeApointment__nameAppointment')
    ordering_fields = ('__all__')

    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_medical_record_to_pdf(self, request, pk=None):
        medical_record = get_object_or_404(MedicalRecords, pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="medical_record_{medical_record.id}.pdf"'
        y = 670

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(f"Historia Clínica de {medical_record.idPatient.firstName} {medical_record.idPatient.lastName}")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exportar Historia Clínica"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(100, 700, "DETALLES")

        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(100, y, f"Cédula: {medical_record.idPatient.Cedula}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Paciente: {medical_record.idPatient.firstName} {medical_record.idPatient.lastName}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Teléfono: {medical_record.idPatient.phone}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Email: {medical_record.idPatient.email}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Seguro: {medical_record.idPatient.insurance_entity}")
        y -= 20

        estado_seguro = "Valid" if medical_record.idPatient.Policy_state else "Expired"

        pdf_canvas.drawString(100, y, f"Estado Seguro: {estado_seguro}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Profesional: {medical_record.idEmployees.firstName} {medical_record.idEmployees.lastName}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Tipo Cita: {medical_record.idTypeAppointment.nameAppointment}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Descripción: {medical_record.description}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Fecha Creación: {medical_record.dateCreated.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 20
        
        pdf_canvas.save()

        return response
    
    @action(detail=False, methods=['get'], url_path='export-all-pdf')
    def export_all_medical_records_to_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_medical_records.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle("Exportación Historias Clínicas")
        pdf_canvas.setFont("Helvetica-Bold", 14)

        title_text = "Historias Clínicas"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(100, 700, "INFORMACIÓN GENERAL HISTORIAS CLÍNICAS")

        pdf_canvas.setFont("Helvetica", 10)
        y = 670
        for medical_record in MedicalRecords.objects.all():
            if y < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 10)
                y = 750

            pdf_canvas.drawString(100, y, f"Cédula: {medical_record.idPatient.Cedula}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Paciente: {medical_record.idPatient.firstName} {medical_record.idPatient.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Teléfono: {medical_record.idPatient.phone}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Email: {medical_record.idPatient.email}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Seguro: {medical_record.idPatient.insurance_entity}")
            y -= 20
            estado_seguro = "Valid" if medical_record.idPatient.Policy_state else "Expired"
            pdf_canvas.drawString(100, y, f"Estado Seguro: {estado_seguro}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Profesional: {medical_record.idEmployees.firstName} {medical_record.idEmployees.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Tipo Cita: {medical_record.idTypeAppointment.nameAppointment}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Descripción: {medical_record.description}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Fecha Creación: {medical_record.dateCreated.strftime('%Y-%m-%d %H:%M:%S')}")
            y -= 20
            pdf_canvas.drawString(100, y, f"------------------------------------------------------------------")
            y -= 10

        pdf_canvas.save()

        return response