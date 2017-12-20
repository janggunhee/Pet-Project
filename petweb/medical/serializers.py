from rest_framework import serializers

from account.serializers import PetSpeciesField
from .models import VaccineInoculation, Vaccine


# 주변 병원 검색 시리얼라이저
class HospitalSerializer(serializers.Serializer):
    lat = serializers.CharField()
    lng = serializers.CharField()


# 백신의 정보를 보여주는 시리얼라이저
class VaccineInfoSerializer(serializers.ModelSerializer):
    species = PetSpeciesField()

    class Meta:
        model = Vaccine
        fields = (
            'species',
            'name',
            'turn',
            'period',
        )


# 동물이 맞은 백신 정보를 보여주는 시리얼라이저
class VaccineInoculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineInoculation
        fields = (
            'medical',
            'vaccine',
            'num_of_times',
            'inoculated_date',
            'hospital',
            'is_alarm',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'vaccine_info': VaccineInfoSerializer(instance.vaccine).data,
            'inoculation_info': ret
        }
        return data
