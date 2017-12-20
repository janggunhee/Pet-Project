from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import near_by_search
from utils.rest_framework import permissions
from .models import PetMedical
from .serializers import HospitalSerializer, VaccineInoculationSerializer


# 주변 병원을 검색해주는 뷰
class Hospital(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            result = near_by_search(
                lat=serializer.data['lat'],
                lng=serializer.data['lng'],
            )
            data = []
            for item in result:
                hospital = {
                    'name': item.name,
                    'address': item.address,
                    'phone': item.phone,
                    'distance': item.distance,
                    'lat': item.h_lat,
                    'lng': item.h_lng,

                }
                data.append(hospital)

            return Response(data, status=status.HTTP_200_OK)
        result = {
            "message": "The hospital search failed. Please check latitude / longitude value.",
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


# 펫이 맞은 백신을 검색해주는 뷰
class PetVaccineInoculation(generics.ListCreateAPIView):
    serializer_class = VaccineInoculationSerializer
    permission_classes = (permissions.IsMedicalOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.inoculation_set.all()
