from rest_framework import serializers
from .models import Medicines, Pharmacy

class MedicineSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Medicines
        fields = '__all__'

class PharmacySerializer(serializers.ModelSerializer) :
    class Meta :
        model = Pharmacy
        fields = '__all__'