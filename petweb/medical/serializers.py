from rest_framework import serializers
from rest_framework.settings import api_settings

from account.serializers import PetSpeciesField
from .models import Inoculation, Vaccine, PetMedical, Operation, BodySize


# ---------- 병원 ---------- #

# 주변 병원 검색 시리얼라이저
class HospitalSerializer(serializers.Serializer):
    lat = serializers.CharField()
    lng = serializers.CharField()


# ---------- 백신 ---------- #

# 백신 이름을 보여주는 관계 필드
class VaccineInfoField(serializers.RelatedField):
    queryset = Vaccine.objects.all()

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        pet_type, vaccine_name = data.replace(' ', '').split(',')
        return Vaccine.objects.filter(species__pet_type=pet_type).get(name=vaccine_name)


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
class InoculationSerializer(serializers.ModelSerializer):
    medical = serializers.CharField(read_only=True)
    vaccine = VaccineInfoField()
    num_of_times = serializers.IntegerField()
    inoculated_date = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT)
    hospital = serializers.CharField(allow_blank=True)
    is_alarm = serializers.BooleanField(default=False)

    class Meta:
        model = Inoculation
        fields = (
            'medical',
            'pk',
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


# ---------- 수술 ---------- #

# 동물의 수술 정보를 보여줘는 시리얼라이저
class OperationSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format=api_settings.DATE_FORMAT, allow_null=True)
    description = serializers.CharField(max_length=70, required=True)
    comment = serializers.CharField(max_length=500, allow_blank=True)

    class Meta:
        model = Operation
        fields = (
            'pk',
            'image',
            'date',
            'description',
            'comment',
        )


# ---------- 사이즈 ---------- #
# 동물의 신체 사이즈를 보여주는 시리얼라이저
class BodySizeSerializer(serializers.ModelSerializer):
    goal_weight = serializers.FloatField(min_value=0)
    current_weight = serializers.FloatField(min_value=0)
    chest = serializers.IntegerField(min_value=0)
    neck = serializers.IntegerField(min_value=0)

    class Meta:
        model = BodySize
        fields = (
            'pk',
            'goal_weight',
            'current_weight',
            'chest',
            'neck',
            'created_date',
        )


# ---------- 종합 ---------- #
# 동물 의료 정보 디테일 시리얼라이저
class PetMedicalDetailSerializer(serializers.ModelSerializer):
    pet = serializers.SlugRelatedField(read_only=True, slug_field='name')
    inoculation_set = InoculationSerializer(read_only=True, many=True)
    operation_set = OperationSerializer(read_only=True, many=True)
    body_size_set = BodySizeSerializer(read_only=True, many=True)

    class Meta:
        model = PetMedical
        fields = (
            'pet',
            'inoculation_set',
            'operation_set',
            'body_size_set',
        )
