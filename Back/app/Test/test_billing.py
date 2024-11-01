from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from ..Billing.models import Billing
from ..MedicalRecords.models import MedicalRecords
from ..Patients.models import Patients
from ..Employees.models import Employees
from ..TypeAppointment.models import TypeAppointment

class BillingTests(APITestCase):

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
            nameAppointment = "Cita revisión general",
            cost = 10.500
        )
        
        self.medical_record = MedicalRecords.objects.create(
            idPatient=self.patient, 
            description="Consulta General",
            idEmployees=self.employee, 
            idTypeAppointment=self.type_appointment
        )

        self.billing = Billing.objects.create(
            idPatients=self.patient,
            idMedicalRecords=self.medical_record,
            totalAmount=100.00,
            paymentStatus=Billing.PaymentStatus.PEND
        )

    def test_list_billings(self):
        url = reverse('Billing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_billing_detail(self):
        url = reverse('Billing-detail', args=[self.billing.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idPatients'], self.patient.id)
        self.assertEqual(response.data['idMedicalRecords'], self.medical_record.id)

    def test_create_billing(self):
        url = reverse('Billing-list')
        data = {
            'idPatients': self.patient.id,
            'idMedicalRecords': self.medical_record.id,
            'totalAmount': 50.25,
            'paymentStatus': Billing.PaymentStatus.PEND
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Billing.objects.count(), 2)

    def test_update_billing(self):
        url = reverse('Billing-detail', args=[self.billing.id])
        data = {
            'paymentStatus': Billing.PaymentStatus.PAG
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.billing.refresh_from_db()
        self.assertEqual(self.billing.paymentStatus, Billing.PaymentStatus.PAG)

    def test_delete_billing(self):
        url = reverse('Billing-detail', args=[self.billing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Billing.objects.count(), 0)
