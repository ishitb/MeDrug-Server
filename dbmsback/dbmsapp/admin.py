from django.contrib import admin
from .models import Medicines, Pharmacy, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class PharmacyAdmin(admin.ModelAdmin) :
    search_fields = ['category']

class MedicinesAdmin(admin.ModelAdmin) :
    search_fields = ['name', 'category__category']
    list_display = ('name', 'category', 'quantity', 'price')

class CustomUserAdmin(UserAdmin) :
    model = UserAdmin
    list_display = ('email', 'first_name', 'last_name', 'snu_id', 'is_staff',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'snu_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'snu_id')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(Medicines, MedicinesAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
