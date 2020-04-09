from rest_framework import serializers
from .models import Medicines, Pharmacy, Doctor

class MedicineSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Medicines
        fields = '__all__'

class PharmacySerializer(serializers.ModelSerializer) :
    class Meta :
        model = Pharmacy
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Doctor
        fields = '__all__'