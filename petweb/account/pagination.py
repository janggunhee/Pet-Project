from rest_framework.pagination import PageNumberPagination


class StandardPetViewPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000
