from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointments

class DoctorResource(resources.ModelResource):
    class Meta:
        model = Doctor 


class DoctorScheduleResource(resources.ModelResource):
    class Meta:
        model = DoctorSchedule

class PharmacyResource(resources.ModelResource):
    class Meta:
        model = Pharmacy

class MedicinesResource(resources.ModelResource):
    class Meta:
        model = Medicines

class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser

class DoctorAdmin(ImportExportModelAdmin):
    resource_class = DoctorResource
    search_fields = ['name', 'speciality']
    list_display = ('name', 'id', 'speciality', 'phone')

class ScheduleAdmin(ImportExportModelAdmin) :
    resource_class = DoctorScheduleResource
    list_display = ('time', 'id', 'doctor', 'doctor_id')
    search_fields = ('doctor__name',)

class PharmacyAdmin(ImportExportModelAdmin) :
    resource_class = PharmacyResource
    search_fields = ['category']

class MedicinesAdmin(ImportExportModelAdmin) :
    resource_class = MedicinesResource
    search_fields = ['name', 'category__category']
    list_display = ('name', 'category', 'quantity', 'price')

def superUser(ImportExportModelAdmin, request, queryset) :
    '''
    Create exisiting user to superuser
    '''
    queryset.update(is_superuser=True)
    queryset.update(is_staff=True)

class CustomUserAdmin(ImportExportModelAdmin) :
    resource_class = CustomUserResource
    model = UserAdmin
    list_display = ('email', 'first_name', 'last_name', 'snu_id', 'is_staff', 'id')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'snu_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'snu_id')}
        ),
    )
    search_fields = ('email', 'id')
    ordering = ('email',)
    actions = (superUser, )

class AppointmentAdmin(ImportExportModelAdmin):
     resource_class = AppointmentResource
     search_fields = ['patient__first_name', 'scheduled__time']
     list_display = ['patient', 'snu_id', 'scheduled', 'date', 'docName']

class AlertsAdmin(ImportExportModelAdmin) :
    resource_class = Alerts
    search_fields = ['title', ]
    list_display = ['title', 'link']


# class AppointmentsManager(admin.ModelAdmin) :
#     search_fields = ['patient__first_name', 'doctor__name', 'scheduled__time']
#     list_display = ['patient', 'snu_id', 'doctor', 'scheduled', 'date']



admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Medicines, MedicinesAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorSchedule, ScheduleAdmin)
admin.site.register(Appointments, AppointmentAdmin)
admin.site.register(Alerts, AlertsAdmin)