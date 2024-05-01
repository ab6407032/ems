from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
import json
from django.db.models import Q
#from common.views import UUIDModelViewSet

class DataTablePagination(LimitOffsetPagination):
        limit_query_param = 'length'
        offset_query_param = 'start'

class DataTableListCreateApi(generics.ListCreateAPIView):
    """
    Base Class for DataTable Rest api server

    Provides support for datatable searching and sorting at server-side

    pass field names in search_parameters of all fields to be searched
    for the entered search query in datatable
    """
    pagination_class = DataTablePagination
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None

    def get_queryset(self):
        self.unfiltered_query_set = query_set = super(DataTableListCreateApi, self).get_queryset()

        order_by_index = int(self.request.query_params.get('order[0][column]', 0))
        orderable = bool(self.request.query_params.get('columns[{}][orderable]'.format(order_by_index), 'false'))

        if order_by_index == 0 or not orderable:
            order_by_index = 1

        order_by = self.request.query_params.get('columns[{}][data]'.format(order_by_index), self.default_order_by).replace('.', '__')
        order_by_dir = self.request.query_params.get('order[0][dir]', 'asc')
        if order_by_dir == 'desc':
            order_by = '-{}'.format(order_by)

        search = json.loads(self.request.query_params.get('search'))
        search_queries = search['value']

        q = Q()
        print(self.search_parameters)
        if len(search_queries) > 0:
            for params in self.search_parameters:
                temp = {
                    '{}__contains'.format(params): search_queries,
                }
                q |= Q(**temp)


        query_set = query_set.filter(q)

        if order_by == '':
            return query_set

        return query_set.order_by(order_by)

    def get(self, request, *args, **kwargs):
        result = super(DataTableListCreateApi, self).get(request, *args, **kwargs)
        result.data['draw'] = int(request.query_params.get('draw', 0))

        result.data['recordsFiltered'] = result.data['count']
        result.data['recordsTotal'] = self.unfiltered_query_set.count()
        del result.data['count']

        result.data['data']= result.data['results']
        del result.data['results']
        return result
