from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.functions import near_by_search
from utils.rest_framework import permissions
from .models import PetMedical, Vaccine
from .serializers import HospitalSerializer, \
    VaccineInoculationSerializer, \
    VaccineInfoSerializer, \
    PetMedicalDetailSerializer, PetOperationSerializer, PetSizeSerializer


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


# 펫이 맞은 백신 리스트 / 생성 뷰
class PetVaccineInoculation(generics.ListCreateAPIView):
    serializer_class = VaccineInoculationSerializer
    permission_classes = (permissions.IsMedicalOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.inoculation_set.all()

    def perform_create(self, serializer):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        # May raise a permission denied
        self.check_object_permissions(self.request, instance)
        serializer.save(medical=instance)


# 펫이 맞은 백신 디테일 / 수정 / 삭제 뷰
class PetVaccineInoculationUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VaccineInoculationSerializer
    permission_classes = (permissions.IsHealthInfoOwnerOrReadOnly,)
    lookup_url_kwarg = 'ino_pk'

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.inoculation_set.all()


# 펫의 수술 정보 리스트 / 생성 뷰
class PetOperation(generics.ListCreateAPIView):
    serializer_class = PetOperationSerializer
    permission_classes = (permissions.IsMedicalOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.operation_set.all()

    def perform_create(self, serializer):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        # May raise a permission denied
        self.check_object_permissions(self.request, instance)
        serializer.save(medical=instance)


# 펫의 신체 사이즈 리스트 / 생성 뷰
class PetSize(generics.ListCreateAPIView):
    serializer_class = PetSizeSerializer
    permission_classes = (permissions.IsMedicalOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        return instance.pet_size_set.all()

    def perform_create(self, serializer):
        user = self.kwargs['user_pk']
        pet = self.kwargs['pet_pk']
        instance = PetMedical.objects.filter(pet__owner_id=user).get(pet_id=pet)
        # May raise a permission denied
        self.check_object_permissions(self.request, instance)
        serializer.save(medical=instance)


# 동물 의료 정보 디테일 뷰
class PetMedicalDetail(generics.RetrieveAPIView):
    serializer_class = PetMedicalDetailSerializer
    lookup_field = 'pet_id'
    lookup_url_kwarg = 'pet_pk'

    def get_queryset(self):
        user = self.kwargs['user_pk']
        return PetMedical.objects.filter(pet__owner_id=user)
