from django.shortcuts import get_list_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly
from ..pagination import StandardPetViewPagination
from ..models import Pet
from ..serializers import PetSerializer

__all__ = (
    'PetListCreate',
)


"""
generics.RetrieveUpdateDestroyAPIView
3. 하나의 펫을 디테일하게 보는 뷰 (get)
4. 펫의 내용을 수정하는 뷰 (patch)
    1. 수정용 시리얼라이저 필요
5. 펫을 삭제하는 뷰 (delete)

"""


class PetListCreate(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = StandardPetViewPagination
    permission_classes = (IsOwnerOrReadOnly, )
    lookup_url_kwarg = 'user_pk'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_object(self):
        filter_kwargs = {'owner_id': self.kwargs[self.lookup_url_kwarg]}
        obj = get_list_or_404(self.get_queryset(), **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if str(request.user.pk) == request.resolver_match.kwargs['user_pk']:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        error = {
            "detail": "You do not have permission to perform this action."
        }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class PetProfileUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    lookup_url_kwarg = 'user_pk'
