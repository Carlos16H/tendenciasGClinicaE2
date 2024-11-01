from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from ..Patients.models import Patients
from ..Employees.models import Employees

class PatientsTests(APITestCase):

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

    def test_list_patients(self):
        url = reverse('Patients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_patient_detail(self):
        url = reverse('Patients-detail', args=[self.patient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.patient.email)

    def test_create_patient(self):
        url = reverse('Patients-list')
        data = {
            'firstName': "Deivi", 
            'lastName': "Salcedo", 
            'birthDate': "1990-05-05", 
            'gender': Patients.Gender.MALE,
            'policy_validity': '2025-12-31',
            'email': 'deivisalcedo@test.com', 
            'phone': '987654321',
            'address': 'Calle 2 #456 - 789',
            'emergency_contact': 'John Hernandez',
            'insurance_entity': 'VIVA SALUD'
        }
        response = self.client.post(url, data, format='json')
        #print(response.data)  #respuesta detallada en caso de error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patients.objects.count(), 2)

    #Actualiza o elimina pacientes basado en su id
    def test_update_patient(self):
        url = reverse('Patients-detail', args=[self.patient.id])
        data = {
            'email': "janeth.updated@test.com" 
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db() #actualiza registro en bdd
        self.assertEqual(self.patient.email, "janeth.updated@test.com")

    def test_delete_patient(self):
        url = reverse('Patients-detail', args=[self.patient.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patients.objects.count(), 0)

    def test_export_patient_to_pdf(self):
        url = reverse('Patients-export-patient-information', args=[self.patient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_export_all_patients_to_pdf(self):
        url = reverse('Patients-export-all-patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')