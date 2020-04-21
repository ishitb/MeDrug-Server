from django.contrib import admin
from .models import Medicines, Pharmacy, CustomUser, Doctor, DoctorSchedule, Appointments
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class DoctorAdmin(admin.ModelAdmin) :
    search_fields = ['name', 'speciality']
    list_display = ('name', 'id', 'speciality', 'phone')

class ScheduleAdmin(admin.ModelAdmin) :
    list_display = ('time', 'doctor',)
    search_fields = ('doctor__name',)

class PharmacyAdmin(admin.ModelAdmin) :
    search_fields = ['category']

class MedicinesAdmin(admin.ModelAdmin) :
    search_fields = ['name', 'category__category']
    list_display = ('name', 'category', 'quantity', 'price')

def superUser(ModelAdmin, request, queryset) :
    '''
    Create exisiting user to superuser
    '''
    queryset.update(is_superuser=True)
    queryset.update(is_staff=True)

class CustomUserAdmin(UserAdmin) :
    model = UserAdmin
    list_display = ('email', 'first_name', 'last_name', 'snu_id', 'is_staff',)
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
    search_fields = ('email',)
    ordering = ('email',)
    actions = (superUser, )

class AppointmentsManager(admin.ModelAdmin) :
    search_fields = ['patient__first_name', 'doctor__name', 'scheduled__time']
    list_display = ['patient', 'snu_id', 'doctor', 'scheduled', 'date']

admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Medicines, MedicinesAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorSchedule, ScheduleAdmin)
admin.site.register(Appointments, AppointmentsManager)