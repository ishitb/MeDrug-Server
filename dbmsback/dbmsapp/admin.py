from django.contrib import admin
from .models import Medicines, Pharmacy

# Register your models here.

class PharmacyAdmin(admin.ModelAdmin) :
    search_fields = ['category']

class MedicinesAdmin(admin.ModelAdmin) :
    search_fields = ['name', 'category__category']
    list_display = ('name', 'category', 'quantity', 'price')

admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Medicines, MedicinesAdmin)
