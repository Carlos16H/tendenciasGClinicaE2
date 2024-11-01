from rest_framework import serializers
from .models import *

class medicineInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicineInventory
        fields = '__all__'