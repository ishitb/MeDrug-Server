from rest_framework import serializers
from .models import Medicines, Pharmacy, Doctor, DoctorSchedule, Appointments

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

class ScheduleSerializer(serializers.ModelSerializer) :
    class Meta :
        model = DoctorSchedule
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Appointments
        fields = '__all__'