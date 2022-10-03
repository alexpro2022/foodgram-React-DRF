from rest_framework.pagination import PageNumberPagination


class CustomPageLimitPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
