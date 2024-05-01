from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.pagination import LimitOffsetPagination

class DataTablePagination(LimitOffsetPagination):
        limit_query_param = 'length'
        offset_query_param = 'start'

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        page_size = self.page_size
        if 'page_size' in self.request.query_params:
            page_size = self.request.query_params['page_size']
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': page_size,
            'results': data
        })

    def get_non_paginated_response(self, data):
        return Response({
            'results': data
        })
