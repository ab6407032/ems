from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        print(request.GET.getlist('search_fields', []))
        return request.GET.getlist('search_fields', [])

class Filter(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset
