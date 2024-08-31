import json
import operator
from functools import reduce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from filters import DynamicSearchFilter, Filter
from paginator import CustomPagination
from notification.models import Template
from notification.serializers import TemplateSerializer
from common.views import UUIDModelViewSet

class TemplateViewset(UUIDModelViewSet):
    queryset = Template.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = TemplateSerializer
    serializer_classes = {
        'list': TemplateSerializer,
        'retrieve': TemplateSerializer,
        'create': TemplateSerializer,
        'retrieve': TemplateSerializer,
        'destroy': TemplateSerializer,
    }
    # pagination_class = CustomPagination
    filter_backends = (DynamicSearchFilter,)
    search_parameters = (
        'used_for', 
        'name',
        'status',
        'active'
    )  # state searchable fields
    default_order_by = 'id'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset
