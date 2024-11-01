from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..MedicalRMedicineI.models import MedicalRMedicineI
from ..MedicalRecords.models import MedicalRecords
from ..medicineInventory.models import MedicineInventory
from ..TypeAppointment.models import TypeAppointment
from ..Patients.models import Patients
from ..Employees.models import Employees

class MedicalRMedicineITests(APITestCase):

    def setUp(self):
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

        refresh = RefreshToken.for_user(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

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
            nameAppointment = "Cita Psiquiatría",
            cost = 30.200
        )

        self.medical_record = MedicalRecords.objects.create(
            idPatient=self.patient, 
            description="Consulta General",
            idEmployees=self.employee, 
            idTypeAppointment=self.type_appointment
        )

        self.medicine_inventory = MedicineInventory.objects.create(
            nameMedicine="Morfina", 
            description = 'Medicamento Analgésico Opioide para calmar el dolor.',
            quantityAvailable=100, 
            cost=150.000
        )

        self.medical_r_medicine_i = MedicalRMedicineI.objects.create(
            idMedicalRecords=self.medical_record,
            idMedicineInventory=self.medicine_inventory,
            amount=2
        )

    def test_list_medical_r_medicine_i(self):
        url = reverse('MedicalRMedicineI-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_medical_r_medicine_i_detail(self):
        url = reverse('MedicalRMedicineI-detail', args=[self.medical_r_medicine_i.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idMedicalRecords'], self.medical_record.id)

    def test_create_medical_r_medicine_i(self):
        url = reverse('MedicalRMedicineI-list')
        data = {
            'idMedicalRecords': self.medical_record.id,
            'idMedicineInventory': self.medicine_inventory.id,
            'amount': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalRMedicineI.objects.count(), 2)

    def test_update_medical_r_medicine_i(self):
        url = reverse('MedicalRMedicineI-detail', args=[self.medical_r_medicine_i.id])
        data = {
            'amount': 5
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medical_r_medicine_i.refresh_from_db()
        self.assertEqual(self.medical_r_medicine_i.amount, 5)

    def test_delete_medical_r_medicine_i(self):
        url = reverse('MedicalRMedicineI-detail', args=[self.medical_r_medicine_i.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalRMedicineI.objects.count(), 0)


