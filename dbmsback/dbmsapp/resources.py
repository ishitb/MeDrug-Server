from import_export import resources
from .models import Appointments

class PersonResource(resources.ModelResource):
    class Meta:
        model = Appointments