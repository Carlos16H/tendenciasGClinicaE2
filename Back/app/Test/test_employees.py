from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from ..Employees.models import Employees

class EmployeesTests(APITestCase):

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

    def test_list_employees(self):
        url = reverse('Employees-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_employee_detail(self):
        url = reverse('Employees-detail', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.employee.email)

    def test_create_employee(self):
        url = reverse('Employees-list')
        data = {
            'firstName': "Jane", 'lastName': "Doe", 'email': "jane.doe@test.com",
            'phone': "0987654321", 'birthdate': "1992-02-02", 
            'address': "Another Address", 'username': "janedoe", 'password': "testpass", 'rol': "ENF"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employees.objects.count(), 2)

    def test_update_employee(self):
        url = reverse('Employees-detail', args=[self.employee.id])
        data = {
            'email': "john.updated@test.com"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.email, "john.updated@test.com")

    def test_delete_employee(self):
        url = reverse('Employees-detail', args=[self.employee.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employees.objects.count(), 0)
