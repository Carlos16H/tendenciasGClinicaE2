from rest_framework.routers import DefaultRouter
from ..medicineInventory.views import *
from ..Employees.views import *
from ..Patients.views import *
from ..MedicalRecords.views import *
from ..Billing.views import *
from ..Appointment.views import *
from ..MedicalRMedicineI.views import *
from ..TypeAppointment.views import *

router = DefaultRouter()

#define your path here 
router.register(r'medicineInventory', medicineInventoryViewset, basename='Inventory')
router.register(r'Employees', EmployeesViewSet, basename='Employees')
router.register(r'Patients', PatientsViewSet, basename='Patients')
router.register(r'MedicalRecords', MedicalRecordViewSet, basename='MedicalRecords')
router.register(r'Billing', BillingsViewSet, basename='Billing')
router.register(r'Appointment', AppointmentsViewSet, basename='Appointment')
router.register(r'MedicalRMedicineI', MedicalRMedicineIViewSet, basename='MedicalRMedicineI')
router.register(r'TypeAppointment', TypeAppointmentViewSet, basename='TypeAppointment')

urlpatterns = router.urls 