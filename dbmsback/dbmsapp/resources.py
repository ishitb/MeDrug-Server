from import_export import resources
from .models import Appointments

class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointments