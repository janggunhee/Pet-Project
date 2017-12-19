from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import near_by_search
from .serializers import HospitalSerializer


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
            "message": "병원 검색에 실패했습니다. 위도/경도 값을 확인해 주세요.",
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
