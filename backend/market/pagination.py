from rest_framework.pagination import PageNumberPagination


class CustomLimitOffsetPagination(PageNumberPagination):
    page_size_query_param = 'limit'

    max_page_size = 50

    # page_query_param = 'cursor'
