from django.urls import path, include
from .views import MedicineViewSet, PharmacyViewSet, Register, Login, contact_upload, DoctorViewSet, ScheduleViewSet, DoctorInfo, DoctorTimings, AppointmentViewSet, userLogin, Home, AlertsViewSet, AppointmentsToSchedule
from rest_framework.routers import DefaultRouter

# FOR IMAGES
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register('pharmacy', PharmacyViewSet, basename="Pharmacy Categories")
router.register('medicines', MedicineViewSet, basename="Medicines")
router.register('doctors', DoctorViewSet, basename="Doctors")
# router.register(r'^schedule/(?P<pk>[^/.]+)', ScheduleViewSet, basename="Timings for Doctors")
router.register('appointment', AppointmentViewSet, basename="Appointments")
# router.register('users', GetUser, basename="Users")
router.register('alerts', AlertsViewSet, basename="Alerts")

urlpatterns = [
    # path('', include(router.urls)),
    path('', Home),
    path('register/', Register),
    path('login/', Login), 
    path('upload/',contact_upload),
    path('info/',DoctorInfo),
    path('timings/',DoctorTimings),
    path('schedule/<int:doctor>/<str:day>/<str:date>/', ScheduleViewSet),
    path('userlogin/<str:email>/', userLogin),
    path('getScheduleData/<int:scheduled_id>', AppointmentsToSchedule)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls