from django.urls import path, include
from .views import MedicineViewSet, PharmacyViewSet, Register, Login, contact_upload, DoctorViewSet, ScheduleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pharmacy', PharmacyViewSet, basename="Pharmacy Categories")
router.register('medicines', MedicineViewSet, basename="Medicines")
router.register('doctors', DoctorViewSet, basename="Doctors")
router.register('schedule', ScheduleViewSet, basename="Timeings for Doctors")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', Register),
    path('login/', Login), 
    path('upload/',contact_upload)  
]