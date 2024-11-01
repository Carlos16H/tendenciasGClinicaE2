from django.apps import AppConfig


class MedicalrmedicineiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.MedicalRMedicineI'
    
    def ready (self):
        from . import receivers