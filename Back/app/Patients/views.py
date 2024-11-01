from django.http import HttpResponse
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import Patients
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PatientsSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class PatientsViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = ([JWTAuthentication])
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    filterset_fields = ("__all__")
    search_fields = ('firstName', 'lastName', 'email', 'username')
    ordering_fields = ('__all__')


    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_patient_information(self, request, pk=None):

       
        #Obtener el paciente usando el pk, en caso de que no se encuentre Error 404
        paciente = get_object_or_404(Patients, pk=pk)

        #Crear la respuesta HTTP que retornará la función, será lo que devolverá la vista
        response = HttpResponse(content_type='application/pdf')

        #Se une el primer y segundo nombre para nombrar el PDF
        response['Content-Disposition'] = f'attachment; filename="{paciente.firstName}_{paciente.lastName}.pdf"'

        '''
        Acá creo un Canvas que es un objeto en blanco donde puedo dibujar texto,
        imagenes y similares, los cuales guardaré como PDF. Le envío response que
        es lo que acabamos de definir arriba (response) y el pagesize es el tamaño de 
        página, que es de los más comunes en PDF.

        '''
        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(f"Información de {paciente.firstName} {paciente.lastName}")

        #TITULO:
        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Información Paciente PDF"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)
        

        y = 750  #coordenada vertical en el documento (para ubicarse)
        pdf_canvas.setFont("Helvetica-Bold", 12)
        y -= 30
        pdf_canvas.drawString(100, y, f"INFORMACIÓN DEL PACIENTE")
        y -= 20  # y -= 20 es solo para dar espacio entre los textos.
        
        #CAMPOS PACIENTE:

        pdf_canvas.setFont("Helvetica", 10)

        pdf_canvas.drawString(100, y, f"Nombre: {paciente.firstName} {paciente.lastName}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Fecha de nacimiento: {paciente.birthDate}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Género: {paciente.gender}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Dirección: {paciente.address}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Teléfono: {paciente.phone}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Correo: {paciente.email}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Contacto Emergencia: {paciente.emergency_contact}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Teléfono Contacto Emergencia: {paciente.emergency_contact_phone}")
        y -= 20

        pdf_canvas.setFont("Helvetica-Bold", 10)
        pdf_canvas.drawString(100, y, f"INFORMACIÓN SEGURO")
        pdf_canvas.setFont("Helvetica", 10)

        y -= 20
        pdf_canvas.drawString(100, y, f"Entidad: {paciente.insurance_entity}")
        y -= 20
        pdf_canvas.drawString(100, y, f"Número Seguro: {paciente.policy_number}")
        y -= 20
        
        #GUARDAR EL PDF CON LAS MODIFICACIONES REALIZADAS
        pdf_canvas.save()

        #SE RETORNA EL OBJETO CREADO (Archivo PDF)
        return response
    
    @action(detail=False, methods=['get'], url_path='export-all-pdf')
    def export_all_patients(self, request):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Lista_pacientes.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)

        #TITULO:
        pdf_canvas.setFont("Helvetica-Bold", 14)
        title_text = "Exporte Información Pacientes PDF"
        title_width = pdf_canvas.stringWidth(title_text, "Helvetica-Bold", 14)
        pdf_canvas.drawString((letter[0] - title_width) / 2, 750, title_text)

        #CAMPOS:
        pdf_canvas.setFont("Helvetica", 10)
        
        y = 720

        #ITERAR SOBRE EL MODELO DE PACIENTES, PARA ACCEDER A CADA ELEMENTO:
        for paciente in Patients.objects.all():
            y -= 20
            # Si estamos demasiado cerca del borde inferior, crea una nueva pagina
            if y < 50:  
                pdf_canvas.showPage() 
                pdf_canvas.setFont("Helvetica", 10)
                y = 750

            pdf_canvas.setFont("Helvetica-Bold", 12)
            pdf_canvas.drawString(100, y, f"INFORMACIÓN DEL PACIENTE")
            y -= 20

            pdf_canvas.setFont("Helvetica", 10)
            pdf_canvas.drawString(100, y, f"Nombre: {paciente.firstName} {paciente.lastName}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Fecha de nacimiento: {paciente.birthDate}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Género: {paciente.gender}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Dirección: {paciente.address}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Teléfono: {paciente.phone}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Correo: {paciente.email}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Contacto Emergencia: {paciente.emergency_contact}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Teléfono Contacto Emergencia: {paciente.emergency_contact_phone}")
            y -= 20

            pdf_canvas.setFont("Helvetica-Bold", 10)
            pdf_canvas.drawString(100, y, f"INFORMACIÓN SEGURO")
            pdf_canvas.setFont("Helvetica", 10)

            y -= 20
            pdf_canvas.drawString(100, y, f"Entidad: {paciente.insurance_entity}")
            y -= 20
            pdf_canvas.drawString(100, y, f"Número Seguro: {paciente.policy_number}")
            y -= 30

        pdf_canvas.save()

        return response