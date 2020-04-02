from django.shortcuts import render
from .models import Medicines, Pharmacy, CustomUser
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MedicineSerializer, PharmacySerializer
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
