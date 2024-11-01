
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..medicineInventory.models import MedicineInventory
from ..Employees.models import Employees

class MedicineInventoryTests(APITestCase):

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

        self.medicine = MedicineInventory.objects.create(
            nameMedicine="Paracetamol", 
            description = 'Medicamento',
            quantityAvailable=50, 
            cost=12.200
        )

    def test_list_medicine_inventory(self):
        url = reverse('Inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_medicine_inventory_detail(self):
        url = reverse('Inventory-detail', args=[self.medicine.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nameMedicine'], self.medicine.nameMedicine)

    def test_create_medicine_inventory(self):
        url = reverse('Inventory-list')
        data = {
            'nameMedicine': "Acetaminofen", 
            "description": "Pastillas que no sirven pa' na", 
            'quantityAvailable': 30, 
            'cost': 2000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicineInventory.objects.count(), 2)

    def test_update_medicine_inventory(self):
        url = reverse('Inventory-detail', args=[self.medicine.id])
        data = {
            'quantityAvailable': 60
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.quantityAvailable, 60)

    def test_delete_medicine_inventory(self):
        url = reverse('Inventory-detail', args=[self.medicine.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicineInventory.objects.count(), 0)
