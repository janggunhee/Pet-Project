from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.functions import near_by_search
from utils.rest_framework import permissions
from .models import PetMedical, Vaccine
from .serializers import HospitalSerializer, VaccineInoculationSerializer, VaccineInfoSerializer


# 주변 병원을 검색해주는 뷰
class Hospital(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            result = near_by_search(
                input_lat=serializer.data['lat'],
                input_lng=serializer.data['lng'],
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


# 백신 정보를 보여주는 뷰
class VaccineInfoList(generics.GenericAPIView):
    serializer_class = VaccineInfoSerializer

    def get_queryset(self):
        pet_type = self.request.data['species']
        return Vaccine.objects.filter(species__pet_type=pet_type)

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 펫이 맞은 백신을 검색해주는 뷰
class PetVaccineInoculation(generics.ListCreateAPIView):
    serializer_class = VaccineInoculationSerializer
    permission_classes = (permissions.IsMedicalOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.inoculation_set.all()
