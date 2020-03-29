from django.urls import path, include
from .views import PharmacyViewSet, MedicineViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pharmacy', PharmacyViewSet, basename="Pharmacy Categories")
router.register('medicines', MedicineViewSet, basename="Medicines")

urlpatterns = [
    path('', include(router.urls))
]