from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ImproperlyConfigured
from common.languages.en.common import *
from paginator import DataTablePagination, CustomPagination
from django.db.models import Q
import json


class UUIDModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None
    query_set = None
    pagination_class = DataTablePagination

    def list(self, request, version):
        if 'format' in request.GET:
            result = super(UUIDModelViewSet, self).list(request, version)
            params = request.query_params.get('dt_params', None)
            draw = 0
            if params is not None:
                dt_params = json.loads(params)
                print(dt_params)
                draw = int(dt_params.get('draw', 0))
            print(request.query_params)
            result.data['draw'] = draw
            print(result.data['draw'])

            result.data['recordsFiltered'] = result.data['count']
            if self.unfiltered_query_set is not None:
                result.data['recordsTotal'] = self.unfiltered_query_set.count()
            else:
                result.data['recordsTotal'] = 0
            del result.data['count']

            result.data['data'] = result.data['results']
            del result.data['results']
            return result
        else:

            serializer = self.get_serializer(
                self.get_queryset(), many=True, context={'request': request})
            return Response({
                'data': serializer.data
            })

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_queryset(self):
        search_queries = ""
        order_by = ""

        if 'format' in self.request.query_params:
            self.unfiltered_query_set = query_set = super(
                UUIDModelViewSet, self).get_queryset()
            params = self.request.query_params.get('dt_params', None)

            if params is not None:
                dt_params = json.loads(params)
                columns = dt_params['columns']
                order = dt_params['order']
                search = dt_params["search"]
                # print(columns)
                # print(order)
                # print(search)

                if order:
                    order_by_index = int(order[0]["column"])
                    orderable = columns[order_by_index]["orderable"]

                    if order_by_index == 0 or not orderable:
                        order_by_index = 1

                    order_by = columns[order_by_index]["data"]
                    order_by_dir = order[0]["dir"]
                    if order_by_dir == 'desc':
                        order_by = '-{}'.format(order_by)

                if columns:
                    q = Q()
                    for c in columns:
                        if c["searchable"]:
                            # print(c)
                            if type(c["search"]["value"]) == list:
                                q2 = Q()
                                for i in c["search"]["value"]:
                                    if i:
                                        temp_1 = {
                                            c["name"]: i,
                                        }
                                        q2 |= Q(**temp_1)
                                query_set = query_set.filter(q2)

                            else:
                                if c["search"]["value"] != "":
                                    temp = {
                                        c["data"]: c["search"]["value"],
                                    }
                                    q &= Q(**temp)

                    # print(q)
                    query_set = query_set.filter(q)

                if search:
                    search_queries = search["value"]
                    q = Q()
                    # print(search_queries)
                    if len(search_queries) > 0:
                        for params in self.search_parameters:
                            # print(params)
                            temp = {
                                params + '__contains': search_queries,
                            }
                            q |= Q(**temp)

                        query_set = query_set.filter(q).distinct()
                print(query_set.query)

            search = self.request.query_params.get('search', None)

            if search is not None:
                search_queries = search

                q = Q()
                # print(self.search_parameters)
                if len(search_queries) > 0:
                    for params in self.search_parameters:
                        # print(params)
                        temp = {
                            params + '__contains': search_queries,
                        }
                        q |= Q(**temp)

                query_set = query_set.filter(q)

            if order_by == '':
                return query_set

            return query_set.order_by(order_by)
        else:
            q = Q()
            self.unfiltered_query_set = query_set = super(
                UUIDModelViewSet, self).get_queryset()
            # print(query_set)
            search_fields = self.request.GET.getlist('search_fields', [])
            search_queries = self.request.query_params.get('search')
            for params in search_fields:

                temp = {
                    params + '__icontains': search_queries,
                }
                q |= Q(**temp)

                query_set = query_set.filter(q)
            print("hello")
            print(q)
            return query_set


class UUIDFrontendModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None
    pagination_class = DataTablePagination

    def list(self, request, version):
        if 'format' in request.GET:
            result = super(UUIDFrontendModelViewSet,
                           self).list(request, version)
            result.data['draw'] = int(request.query_params.get('draw', 0))

            result.data['recordsFiltered'] = result.data['count']
            result.data['recordsTotal'] = self.unfiltered_query_set.count()
            del result.data['count']

            result.data['data'] = result.data['results']
            del result.data['results']
            return result
        else:
            serializer = self.get_serializer(
                self.get_queryset(), many=True, context={'request': request})
            return Response({
                'data': serializer.data
            })

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_queryset(self):
        search_queries = ""
        order_by = ""

        self.unfiltered_query_set = query_set = super(
            UUIDFrontendModelViewSet, self).get_queryset()

        if 'format' in self.request.query_params:
            params = self.request.query_params.get('dt_params', None)

            if params is not None:
                dt_params = json.loads(params)
                columns = dt_params['columns']
                order = dt_params['order']
                search = dt_params["search"]
                # print(columns)
                # print(order)
                # print(search)

                if order:
                    order_by_index = int(order[0]["column"])
                    orderable = columns[order_by_index]["orderable"]

                    if order_by_index == 0 or not orderable:
                        order_by_index = 1

                    order_by = columns[order_by_index]["data"]
                    order_by_dir = order[0]["dir"]
                    if order_by_dir == 'desc':
                        order_by = '-{}'.format(order_by)

                    if columns:
                        q = Q()

                        for c in columns:
                            if c["searchable"]:
                                # print(c)
                                if type(c["search"]["value"]) == list:
                                    q2 = Q()
                                    for i in c["search"]["value"]:
                                        if i:
                                            temp = {
                                                c["name"]: i,
                                            }
                                            q |= Q(**temp)
                                    query_set = query_set.filter(q)

                                else:
                                    if c["search"]["value"] != "":
                                        temp = {
                                            c["data"]: c["search"]["value"],
                                        }
                                        q &= Q(**temp)

                        # print(q)
                        query_set = query_set.filter(q)

                    if search:
                        search_queries = search["value"]
                        q = Q()
                        # print(search_queries)
                        if len(search_queries) > 0:
                            for params in self.search_parameters:
                                # print(params)
                                temp = {
                                    params + '__contains': search_queries,
                                }
                                q |= Q(**temp)

                            query_set = query_set.filter(q)
                            # print(query_set.query)

            search = self.request.query_params.get('search', None)

            if search is not None:
                search_queries = search

                q = Q()
                # print(self.search_parameters)
                if len(search_queries) > 0:
                    for params in self.search_parameters:
                        # print(params)
                        temp = {
                            params + '__contains': search_queries,
                        }
                        q |= Q(**temp)

                query_set = query_set.filter(q)

            if order_by == '':
                return query_set

            return query_set.order_by(order_by)
        else:
            q = Q()
            self.unfiltered_query_set = query_set = super(
                UUIDFrontendModelViewSet, self).get_queryset()
            print(query_set)
            search_fields = self.request.GET.getlist('search_fields', [])
            search_queries = self.request.query_params.get('search')
            for params in search_fields:

                temp = {
                    params + '__icontains': search_queries,
                }
                q |= Q(**temp)

                query_set = query_set.filter(q)
            return query_set


class FrontEndModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    queryset = None
    unfiltered_query_set = None
    # query_set = None
    pagination_class = CustomPagination

    def list(self, request, version):
        if 'format' in request.GET:
            result = super(FrontEndModelViewSet, self).list(request, version)
            result.data['draw'] = int(request.query_params.get('draw', 0))

            result.data['recordsFiltered'] = result.data['count']
            result.data['recordsTotal'] = self.unfiltered_query_set.count()
            del result.data['count']

            result.data['data'] = result.data['results']
            del result.data['results']
            return result
        else:
            serializer = self.get_serializer(
                self.get_queryset(), many=True, context={'request': request})
            return Response({
                'data': serializer.data
            })

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_queryset(self):
        search_queries = ""
        order_by = ""
        self.unfiltered_query_set = query_set = super(
            FrontEndModelViewSet, self).get_queryset()

        if 'format' in self.request.query_params:

            search = self.request.query_params.get('search', None)

            if search is not None:
                search_queries = search

                q = Q()
                # print(self.search_parameters)
                if len(search_queries) > 0:
                    for params in self.search_parameters:
                        # print(params)
                        temp = {
                            params+"__icontains": search_queries,
                        }
                        q |= Q(**temp)

                query_set = query_set.filter(q)

            if order_by == '':
                return query_set

            return query_set.order_by(order_by)
        else:
            q = Q()
            search_fields = self.request.GET.getlist('search_fields', [])
            search_queries = self.request.query_params.get('search')
            for params in search_fields:

                temp = {
                    '{}__icontains'.format(params): search_queries,
                }
                q |= Q(**temp)

                query_set = query_set.filter(q)

            return query_set

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    # def create(self, request, version):
    #     response = {'message': CREATE_NOT_AUTHORIZED}
    #     return Response(response, status=status.HTTP_403_FORBIDDEN)

    # def update(self, request, version, pk=None):
    #     response = {'message': UPDATE_NOT_AUTHORIZED}
    #     return Response(response, status=status.HTTP_403_FORBIDDEN)

    # def partial_update(self, request, version, pk=None):
    #     response = {'message': PARTIAL_UPDATE_NOT_AUTHORIZED}
    #     return Response(response, status=status.HTTP_403_FORBIDDEN)

class UUIDAltModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None
    pagination_class = CustomPagination
    
    def list(self, request, version):
        if 'format' in request.GET:
            result = super(UUIDAltModelViewSet, self).list(request, version)
            result.data['draw'] = int(request.query_params.get('draw', 0))

            result.data['recordsFiltered'] = result.data['count']
            result.data['recordsTotal'] = self.unfiltered_query_set.count()
            del result.data['count']

            result.data['data'] = result.data['results']
            del result.data['results']
            return result
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
            return Response({
                'data': serializer.data
            })

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_queryset(self):
        search_queries = ""
        order_by = ""

        if 'format' in self.request.query_params:
            self.unfiltered_query_set = query_set = super(UUIDAltModelViewSet, self).get_queryset()
            params = self.request.query_params.get('dt_params', None)
            
            if 'fixed_search' in self.request.query_params:
                fixed_search = self.request.query_params.get('fixed_search')
                if 'field' in self.request.query_params:
                    field = self.request.query_params.get('field')
                    filter_kwargs = {field + '__exact': fixed_search}
                    print(filter_kwargs)
                    query_set = query_set.filter(**filter_kwargs)
            
            if params is not None:
                dt_params = json.loads(params)
                columns = dt_params['columns']
                order = dt_params['order']
                search = dt_params["search"]
                print(columns)
                print(order)
                print(search)

                if order:
                    order_by_index = int(order[0]["column"])
                    orderable = columns[order_by_index]["orderable"]

                    if order_by_index == 0 or not orderable:
                        order_by_index = 1

                    order_by = columns[order_by_index]["data"]
                    order_by_dir = order[0]["dir"]
                    if order_by_dir == 'desc':
                        order_by = '-{}'.format(order_by)

                    if columns:
                        q = Q()

                        for c in columns:
                            if c["searchable"]:
                                print(c["search"]["value"])
                                if type(c["search"]["value"]) == list:
                                    q2 = Q()
                                    for i in c["search"]["value"]:
                                        if i:
                                            temp = {
                                                c["data"] : i,
                                            }
                                            q |= Q(**temp)
                                    query_set = query_set.filter(q)
 
                                else:
                                    if c["search"]["value"] != "":
                                        temp = {
                                            c["data"] : c["search"]["value"],
                                        }
                                        q &= Q(**temp)

                        query_set = query_set.filter(q)
                        print(q)


                    if search:
                        search_queries = search["value"]
                        q = Q()
                        print(search_queries)
                        if len(search_queries) > 0:
                            for params in self.search_parameters:
                                print(params)
                                temp = {
                                    params + '__contains': search_queries,
                                }
                                q |= Q(**temp)

            
                            query_set = query_set.filter(q)
            
            
            
            search = self.request.query_params.get('search', None)

            if search is not None:
                search_queries = search

                q = Q()
                #print(self.search_parameters)
                if len(search_queries) > 0:
                    for params in self.search_parameters:
                        print(params)
                        temp = {
                            params: search_queries,
                        }
                        q |= Q(**temp)

                query_set = query_set.filter(q)

            if order_by == '':
                return query_set

            return query_set.order_by(order_by)
        else:
            q = Q()
            query_set = super(UUIDAltModelViewSet, self).get_queryset()
            search_fields = self.request.GET.getlist('search_fields', [])
            search_queries = self.request.query_params.get('search')
            for params in search_fields:
        
                temp = {
                    '{}'.format(params): search_queries,
                }
                q |= Q(**temp)

                query_set = query_set.filter(q)
  
            return query_set
       

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def create(self, request, version):
        response = {'message': CREATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, version, pk=None):
        response = {'message': UPDATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, version, pk=None):
        response = {'message': PARTIAL_UPDATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, version, pk=None):
        response = {'message': DESTROY_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class UUIDAlt1ModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None
    pagination_class = CustomPagination
    

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
        
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def create(self, request, version):
        response = {'message': CREATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, version, pk=None):
        response = {'message': UPDATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, version, pk=None):
        response = {'message': PARTIAL_UPDATE_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, version, pk=None):
        response = {'message': DESTROY_NOT_AUTHORIZED}
        return Response(response, status=status.HTTP_403_FORBIDDEN)



class UUIDAlt2ModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    search_parameters = ()
    default_order_by = ''
    unfiltered_query_set = None
    pagination_class = CustomPagination
    

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)