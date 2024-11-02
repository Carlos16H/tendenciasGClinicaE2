
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..MedicalRecords.models import MedicalRecords
from ..Patients.models import Patients
from ..TypeAppointment.models import TypeAppointment
from ..Employees.models import Employees

class MedicalRecordsTests(APITestCase):

    def setUp(self):
        #Crear empleado para la autenticación
        self.employee = Employees.objects.create(
            firstName="Demo", 
            lastName="Test", 
            phone='123456789',
            birthdate='1999-01-01',
            address='Calle 1 #234 - 567',
            username="demo",
            password='demo',
            email='demo@test.com',
            rol="ADM",
        )

        self.client = APIClient()

        # Envía credenciales para la autenticación
        refresh = RefreshToken.for_user(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Crea un paciente para las pruebas
        self.patient = Patients.objects.create(
            firstName="Janeth", 
            lastName="Gutierrez", 
            Cedula = '1000876231',
            birthDate="2000-01-01",
            email = 'janeth.gutierrez@test.com',
            gender=Patients.Gender.FEM,
            policy_validity='2024-12-31'
        )

        self.type_appointment = TypeAppointment.objects.create(
            nameAppointment = "Cita Control Materno",
            cost = 30
        )
        
        self.medical_record = MedicalRecords.objects.create(
            idPatient=self.patient, 
            description="Consulta General",
            idEmployees=self.employee, 
            idTypeAppointment=self.type_appointment
        )

    def test_list_medical_records(self):
        url = reverse('MedicalRecords-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_medical_record_detail(self):
        url = reverse('MedicalRecords-detail', args=[self.medical_record.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idPatient'], self.patient.id)

    def test_create_medical_record(self):
        url = reverse('MedicalRecords-list')
        data = {
            'idPatient': self.patient.id,
            'description': "Consulta Nueva",
            'idEmployees': self.employee.id,
            'idTypeAppointment': self.type_appointment.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalRecords.objects.count(), 2)

    def test_update_medical_record(self):
        url = reverse('MedicalRecords-detail', args=[self.medical_record.id])
        data = {
            'description': "Consulta Actualizada"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medical_record.refresh_from_db()
        self.assertEqual(self.medical_record.description, "Consulta Actualizada")

    def test_delete_medical_record(self):
        url = reverse('MedicalRecords-detail', args=[self.medical_record.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalRecords.objects.count(), 0)

    def test_export_medicalrecord_to_pdf(self):
        url = reverse('MedicalRecords-export-medical-record-to-pdf', args=[self.medical_record.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_export_all_medicalrecords_to_pdf(self):
        url = reverse('MedicalRecords-export-all-medical-records-to-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')