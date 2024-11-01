from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..Appointment.models import Appointment
from ..Patients.models import Patients
from ..Employees.models import Employees
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class AppointmentTests(APITestCase):

    #acá normalmente se crea a través de User, pero en nuestro caso
    #es Employees, que es donde creamos el usuario que se logueará.

    def setUp(self):
        self.employee = Employees.objects.create(
            firstName="Demo", 
            lastName="Test", 
            phone = '123456789',
            birthdate = '1999-01-01',
            address = 'Calle 1 #234 - 567',
            username = "demo",
            password = 'demo',
            email = 'demo@test.com',
            rol = "ADM"
        )
        
        self.client = APIClient()

        #se envian credenciales al token para que permita el acceso.
        refresh = RefreshToken.for_user(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.patient = Patients.objects.create(
            firstName = "Janeth", 
            lastName = "Gutierrez", 
            birthDate = "2000-01-01",
            gender = Patients.Gender.FEM,
            policy_validity = '2024-12-31'
    
        )
        
        self.appointment = Appointment.objects.create(
            idPatient=self.patient,
            idEmployee=self.employee,
            datetime=datetime(2024, 10, 27, 10, 0),
            reason="Consulta General",
            status=Appointment.AppointmentStatus.PROGR
        )
        
    #assertEqual: comprueba que los valores sean iguales, sino la prueba falla.
    #assertTrue: comprueba si es verdadero, sino la prueba falla.

    def test_list_appointments(self):
        url = reverse('Appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_appointment_detail(self):
        url = reverse('Appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idPatient'], self.patient.id)
        self.assertEqual(response.data['idEmployee'], self.employee.id)

    def test_update_appointment(self):
        url = reverse('Appointment-detail', args=[self.appointment.id])
        #cita existente, se actualiza el motivo y el estado
        updated_data = {
            "idPatient": self.patient.id,
            "idEmployee": self.employee.id,
            "datetime": "2024-10-27T10:00:00Z",
            "reason": "Consulta Especializada",
            "status": Appointment.AppointmentStatus.COMPL
        }
        response = self.client.patch(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.datetime.strftime('%Y-%m-%dT%H:%M:%SZ'), updated_data['datetime'])
        self.assertEqual(self.appointment.reason, updated_data['reason'])
        self.assertEqual(self.appointment.status, updated_data['status'])

    def test_delete_appointment(self):
        url = reverse('Appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_export_appointment_to_pdf(self):
        url = reverse('Appointment-export-appointment-to-pdf', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_export_all_appointments_to_pdf(self):
        url = reverse('Appointment-export-all-appointments-to-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

