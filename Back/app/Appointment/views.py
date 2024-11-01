from django.http import HttpResponse
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Appointment
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AppointmentsSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentsSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,  
        filters.OrderingFilter,
    ]
    
    filterset_fields = ('__all__')
    search_fields = ('idPatient__firstName', 'idEmployee__firstName', 'datetime','status')
    ordering_fields = ('__all__')

    #permission_classes = [AllowAny]

    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_appointment_to_pdf(self, request, pk=None):
        appointment = get_object_or_404(Appointment, pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="appointment_{appointment.id}.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(f"Cita médica de {appointment.idPatient.firstName} {appointment.idPatient.lastName}")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Información Cita"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(100, 700, "INFORMACIÓN DE LA CITA MÉDICA")
            
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(100, 670, f"Paciente: {appointment.idPatient.firstName} {appointment.idPatient.lastName}")
        pdf_canvas.drawString(100, 650, f"Médico Asignado: {appointment.idEmployee.firstName} {appointment.idEmployee.lastName}")
        pdf_canvas.drawString(100, 630, f"Fecha y Hora: {appointment.datetime.strftime('%Y-%m-%d %H:%M')}")
        pdf_canvas.drawString(100, 610, f"Motivo de la Cita: {appointment.reason}")
        pdf_canvas.drawString(100, 590, f"Estado: {appointment.status}")

        pdf_canvas.save()

        return response
    
    @action(detail=False, methods=['get'], url_path='export-all-pdf')
    def export_all_appointments_to_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_appointments.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle("Listado de Todas las Citas Médicas")

        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Información Citas"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(100, 700, "INFORMACIÓN DE TODAS LAS CITAS MÉDICAS")

        pdf_canvas.setFont("Helvetica", 10)
        y = 670
        for appointment in Appointment.objects.all():
            if y < 50:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 10)
                y = 750

            pdf_canvas.drawString(100, y, f"Paciente: {appointment.idPatient.firstName} {appointment.idPatient.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Médico: {appointment.idEmployee.firstName} {appointment.idEmployee.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Fecha y Hora: {appointment.datetime.strftime('%Y-%m-%d %H:%M')}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Motivo: {appointment.reason}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Estado: {appointment.status}")
            y -= 30

        pdf_canvas.save()

        return response

