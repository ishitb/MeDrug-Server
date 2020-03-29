from django.shortcuts import render
from .models import Medicines, Pharmacy
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MedicineSerializer, PharmacySerializer
from django.http import HttpResponse, JsonResponse

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