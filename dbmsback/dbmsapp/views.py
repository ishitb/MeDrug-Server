from django.shortcuts import render
import csv,io
from tablib import Dataset
from .resources import *
from django.contrib import messages
from .models import Medicines, Pharmacy, CustomUser, Doctor, DoctorSchedule, Appointments, Alerts
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MedicineSerializer, PharmacySerializer, DoctorSerializer, ScheduleSerializer, AppointmentSerializer, UserSerializer, AlertSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, TemplateHTMLRenderer



# Create your views here.

# class PharmacyViewSet(viewsets.ViewSet) :
#     def list(self, request) :
#         category = Pharmacy.objects.all()
#         serializer = PharmacySerializer(category, many=True)
#         return Response(serializer.data) 
    
#     def create(self, request) :
#         serializer = PharmacySerializer(data = request.data)

#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None) :
#         queryset = Pharmacy.objects.all()
#         category = get_object_or_404(queryset, pk=pk)
#         serializer = PharmacySerializer(category)
#         return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

#     def update(self, request, pk) :
#         queryset = Pharmacy.object.all()
#         category = get_object_or_404(queryset, pk=pk) 
#         serializer = PharmacySerializer(category, data = request)

#         if serializer.is_valid() :
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Resposer(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk) :
#         queryset = Pharmacy.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         article.delete()
#         return Response(status = status.HTTP_202_ACCEPTED)


class PharmacyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin) :
    serializer_class = PharmacySerializer
    queryset = Pharmacy.objects.all()

class MedicineViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin) :
    serializer_class = MedicineSerializer
    queryset = Medicines.objects.all()

class DoctorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) :
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

class AlertsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) : 
    serializer_class = AlertSerializer
    queryset = Alerts.objects.all()

# class ScheduleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) :
#     serializer_class = ScheduleSerializer
#     queryset = DoctorSchedule.objects.all()

# class ScheduleViewSet(viewsets.ViewSet) :
#     def retrieve(self, request, pk) :

#         schedule = DoctorSchedule.objects.filter(doctor=pk)
#         serializer = ScheduleSerializer(schedule, many=True)
#         # print("-----------------------")
#         # print(pk)
#         # print("-----------------------")
#         return Response(serializer.data)

@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def ScheduleViewSet(request, doctor, day, date) :
    schedules = DoctorSchedule.objects.filter(doctor=doctor, day=day.capitalize()).values()
    category = Appointments.objects.filter(date=date).values()
    dataSet = category
    booked = []
    for data in dataSet :
        booked.append(data['scheduled_id'])
    for schedule in schedules :
        if schedule['id'] in booked :
            schedule.update({'slot_booked': True})
        else :
            schedule.update({'slot_booked': False})
    return Response(schedules)

# class GetUser(viewsets.ViewSet) :
#     def list(self, request) :
#         users = CustomUser.objects.all()[::-1][0]
#         serializer = UserSerializer(users)
#         data = serializer.data
#         id = {"id": data["id"]}
#         return Response(data)

@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def userLogin(request, email):
    currUser = CustomUser.objects.filter(email=email).values()[0]['id']
    print(currUser)
    return Response({"id": currUser})
    
# class GetUser(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) :
#     serializer_class = UserSerializer
#     queryset = Appointments.objects.all()
    

# class AppointmentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) :
#     serializer_class = AppointmentSerializer
#     queryset = Appointments.objects.all()
#     print("heyy there bro what up")


from django.core.mail import send_mail
from django.conf import settings

class AppointmentViewSet(viewsets.ViewSet) :
    def list(self, request) :
        category = Appointments.objects.all()
        serializer = AppointmentSerializer(category, many=True) 
        return Response(serializer.data) 
    
    def create(self, request) :
        serializer = AppointmentSerializer(data = request.data)

        if serializer.is_valid() :
            serializer.save()

            # SEND AUTOMATED MAIL
            user_email = CustomUser.objects.filter(id=request.data['patient']).values()[0]['email']
            schedule = DoctorSchedule.objects.filter(pk = serializer.data['scheduled']).values()[0]
            doctor = Doctor.objects.filter(pk = schedule['doctor_id']).values()[0]['name']
            send_mail("Appointment with MeDrug", "Your appointment on " + str(request.data["date"]) + ", " + str(schedule['day']) + " at " + str(schedule['time']) + " with " + str(doctor) + " is confirmed.", settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None) :
        queryset = Appointments.objects.all()
        category = Appointments.objects.filter(patient=pk).values()
        dataSet = category
        for data in dataSet :
            schedule_id = data['scheduled_id']
            schedule = DoctorSchedule.objects.filter(pk = schedule_id).values()[0]
            doctor = Doctor.objects.filter(pk = schedule['doctor_id']).values()[0]['name']
            time = schedule['time']
            day = schedule['day']
            data.update({'doctor': doctor, 'time': time, 'day': day})
        return Response(dataSet, status = status.HTTP_202_ACCEPTED)

    def update(self, request, pk) :
        queryset = Appointments.objects.all()
        category = get_object_or_404(queryset, pk=pk) 
        serializer = AppointmentSerializer(category, data = request)

        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk) :
        queryset = Appointments.objects.all()
        article = get_object_or_404(queryset, pk=pk)

        # SEND DELETE EMAIL
        data = Appointments.objects.filter(pk=pk).values()[0]
        user_email = CustomUser.objects.filter(id=data['patient_id']).values()[0]['email']
        schedule = DoctorSchedule.objects.filter(pk = data['scheduled_id']).values()[0]
        doctor = Doctor.objects.filter(pk = schedule['doctor_id']).values()[0]['name']
        send_mail("Cancellation of Appointment with MeDrug", "Your appointment on " + str(data["date"]) + ", " + str(schedule['day']) + " at " + str(schedule['time']) + " with " + str(doctor) + " is successfully cancelled.\nIf this was not you or there is some other problem please contect the front desk via our application.\nThank you.", settings.EMAIL_HOST_USER, [user_email], fail_silently=True)

        article.delete()
        return Response(status = status.HTTP_202_ACCEPTED)




# @api_view(["GET"])
# @renderer_classes([BrowsableAPIRenderer, JSONRenderer])
# def ScheduleViewSet(request, doctor) :
#     schedules = DoctorSchedule.objects.filter(doctor=doctor)
#     serializer = ScheduleSerializer(schedules, many=True)
#     # data = serializer.data
#     print("-----------------------")
#     final = serializer.data
#     print("-----------------------")
#     return Response(final)

# USER REGISTER AND LOGIN
@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
def Register(request, format=None):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    snu_id = request.data.get('snu_id')
    if CustomUser.objects.filter(email=email).exists() :
        # return Response({'status': 'User already exists'})
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    user = CustomUser.objects.create_user(email=email, password=password)
    
    user.first_name = first_name
    user.last_name = last_name
    user.snu_id = snu_id
    user.save()

    # Generate Token for user
    token = Token.objects.create(user=user)

    logged_in_user = CustomUser.objects.filter(email=email).values()[0]
    # return Response({'token': token.key, 'user_data': logged_in_user}, status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_201_CREATED)


# @api_view(["POST"])
# @renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
# @permission_classes((AllowAny,))
# def Login(request):
#     email = request.data.get("email")
#     password = request.data.get("password")

#     user = authenticate(email=email, password=password)
#     if not user:
#         return Response({'error': 'Invalid Credentials', 'status': 'fail'})
#     token, _ = Token.objects.get_or_create(user=user)

#     logged_in_user = CustomUser.objects.filter(email=email).values()[0]

#     # return Response({'token': token.key, 'status': 'success', 'user_data': {
#     #     'email': logged_in_user.get('email'),
#     #     'first_name': logged_in_user.get('first_name'),
#     #     'last_name': logged_in_user.get('last_name'),
#     #     'snu_id': logged_in_user.get('snu_id')
#     # }})
#     return Response({'token': token.key, 'user_data': logged_in_user}, status=status.HTTP_202_ACCEPTED)


# TRYING FOR LOGIN
@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
@permission_classes((AllowAny,))
def Login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)
    if not user:
        return Response({"email": "Invalid Credentials", "password": str(-1)}, status = status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)

    logged_in_user = CustomUser.objects.filter(email=email).values()[0]
    return Response({"email": "success", "password": str(logged_in_user.get('id'))}, status = status.HTTP_202_ACCEPTED)
    # return Response({'token': token.key, 'user_data': logged_in_user}, status=status.HTTP_202_ACCEPTED)


def contact_upload(request):
    template='contact_upload.html'

    prompt={
        'order': 'Category, Name, Quantity, Price',
        'heading': 'New Medicines'.upper()
    }
    if request.method =="GET":
        return render(request,template,prompt)

    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        # _, created = Medicines.objects.update_or_create(
        #     category=column[0],
        #     name=column[1],
        #     quantity=column[2],
        #     price=column[3],
        #     image=column[4]
        # )
        category = column[0]
        name = column[1]
        quantity = column[2]
        price = column[3]
        Medicines.objects.update_or_create(
            name = name,
            quantity = quantity,
            price = price,
            category_id = category
        )
    context = {}

    return render(request,template,context)

def DoctorInfo(request):
    template='doctor_info.html'

    prompt={
        'order':'Name, Phone , Speciality, Picture, Details',
        'heading': "New Doctors' Info".upper()
    }
    if request.method =="GET":
        return render(request,template,prompt)

    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        name = column[0]
        phone = column[1]
        speciality = column[2]
        picture = column[3]
        details = details[4]

        Doctor.objects.update_or_create(
            name = name,
            phone = phone,
            speciality = speciality,
            picture = picture,
            details = details
        )
    context = {}

    return render(request,template,context)

def DoctorTimings(request):
    template='doctor_info.html'

    prompt={
        'order':'Time, Doctor Name',
        'heading': "New Doctors' Schedule".upper()
    }
    if request.method == 'POST':
        person_resource = AppointmentResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now
    
    if request.method =="GET":
        return render(request,template,prompt)

    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        time = column[0]
        doctor = column[1]
      
        DoctorSchedule.objects.update_or_create(
            time = time,
            doctor = doctor,
        )
    context = {}

    return render(request,template,context)

def Home(request) :
    template = 'home.html'
    return render(request, template)

@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
def AppointmentsToSchedule(request, scheduled_id) :
    schedule = DoctorSchedule.objects.filter(pk = scheduled_id).values()[0]
    doctor = Doctor.objects.filter(pk = schedule['doctor_id']).values()[0]
    data = {
        'time': schedule['time'],
        'day': schedule['day'],
        'doctor_name': doctor['name']
    }
    return Response(data, status=status.HTTP_200_OK)