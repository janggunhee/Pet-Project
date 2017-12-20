from rest_framework.pagination import PageNumberPagination

__all__ = (
    'StandardPetViewPagination',
)


class StandardPetViewPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000

class StandardHospitalViewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


