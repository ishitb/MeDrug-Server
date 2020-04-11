from django.shortcuts import render
import csv,io
from django.contrib import messages
from .models import Medicines, Pharmacy, CustomUser, Doctor, DoctorSchedule
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MedicineSerializer, PharmacySerializer, DoctorSerializer, ScheduleSerializer
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

class ScheduleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin) :
    serializer_class = ScheduleSerializer
    queryset = DoctorSchedule.objects.all()

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
        return Response({'status': 'User already exists'})
    
    user = CustomUser.objects.create_user(email=email, password=password)
    
    user.first_name = first_name
    user.last_name = last_name
    user.snu_id = snu_id
    user.save()

    # Generate Token for user
    token = Token.objects.create(user=user)

    logged_in_user = CustomUser.objects.filter(email=user).values()[0]

    return Response(logged_in_user, status = status.HTTP_201_CREATED)

@api_view(["POST"])
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
@permission_classes((AllowAny,))

def Login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials', 'status': 'fail'})
    token, _ = Token.objects.get_or_create(user=user)

    logged_in_user = CustomUser.objects.filter(email=user).values()[0]

    # return Response({'token': token.key, 'status': 'success', 'user_data': {
    #     'email': logged_in_user.get('email'),
    #     'first_name': logged_in_user.get('first_name'),
    #     'last_name': logged_in_user.get('last_name'),
    #     'snu_id': logged_in_user.get('snu_id')
    # }})
    return Response({'token': token.key, 'user_data': logged_in_user}, status=status.HTTP_202_ACCEPTED)


def contact_upload(request):
    template='contact_upload.html'

    prompt={
        'order':'Order of the CSV should be category,name,quantity,price'
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
        'order':'Order of the CSV should be Name, Phone ,Speciality,Picture,details'
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
    template='doctor_timings.html'

    prompt={
        'order':'Order of the CSV should be Time ,Doctor Name'
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
        time = column[0]
        doctor = column[1]
      
        DoctorSchedule.objects.update_or_create(
            time = time,
            doctor = doctor,
        )
    context = {}

    return render(request,template,context)