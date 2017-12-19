from rest_framework import serializers


class HospitalSerializer(serializers.Serializer):
    lat = serializers.CharField()
    lng = serializers.CharField()
