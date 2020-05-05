from django.urls import path, include
from .views import MedicineViewSet, PharmacyViewSet, Register, Login, contact_upload, DoctorViewSet, ScheduleViewSet, DoctorInfo, DoctorTimings, AppointmentViewSet, GetUser, userLogin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pharmacy', PharmacyViewSet, basename="Pharmacy Categories")
router.register('medicines', MedicineViewSet, basename="Medicines")
router.register('doctors', DoctorViewSet, basename="Doctors")
# router.register(r'^schedule/(?P<pk>[^/.]+)', ScheduleViewSet, basename="Timings for Doctors")
router.register('appointment', AppointmentViewSet, basename="Appointments")
router.register('users', GetUser, basename="Users")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', Register),
    path('login/', Login), 
    path('upload/',contact_upload),
    path('info/',DoctorInfo),
    path('timings/',DoctorTimings),
    path('userlogin/<str:email>/', userLogin),
    path('schedule/<int:doctor>/<str:day>/', ScheduleViewSet)
]