from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import pre_save
from django.db import models
import datetime
# Create your models here.

class Doctor(models.Model) :
    name = models.CharField(max_length=50)
    phone = models.IntegerField(null=True)
    speciality = models.CharField(max_length=25, default="General Physician")
    # picture = models.ImageField(null=True,blank = True)
    details = models.CharField(max_length=150,blank = True)

    def __str__(self) :
        return self.name  

class DoctorSchedule(models.Model) :
    time = models.CharField(max_length=50)
    day = models.CharField(max_length=10, default="Monday")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self) :
        return str(self.time + " - " + self.day)  
    def getDoc(self) :
        return self.doctor

class Pharmacy(models.Model) :
    category = models.CharField(max_length=25)
   
    def __str__(self) :
        return self.category


class Medicines(models.Model) :
    category = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    # image = models.ImageField(null=True,blank = True)

    def __str__(self) :
        return self.name

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """


    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25,null=True)
    snu_id = models.CharField(max_length=5)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name
    
    def get_id(self) :
        return self.snu_id

    def getName(self) :
        __str__()

class Appointments(models.Model) :
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scheduled = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
    comments = models.TextField(max_length=200)
    date = models.DateField()

    class Meta :
        unique_together = ('patient', 'scheduled', 'date')

    def snu_id(self) :
        return self.patient.snu_id
    def __str__(self) :
        string = str(self.patient) + " has an appointment with "  + " on " + str(self.date)  + ", " + str(self.scheduled) + " with " + str(self.scheduled.getDoc()) 
        # self.patient + " has an appointment with " + self.doctor 
        return string 
    def docName(self) :
        return self.scheduled.getDoc()