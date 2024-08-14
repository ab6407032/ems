import json
import operator
from functools import reduce
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from filters import DynamicSearchFilter, Filter
from paginator import CustomPagination
from common.serializers import EmptySerializer
from monitor.models import Node
from monitor.serializers import NodeSerializer
from common.views import UUIDAltModelViewSet
from rest_framework.parsers import (MultiPartParser, JSONParser)

class NodeMonitorViewset(UUIDAltModelViewSet):
    queryset = Node.objects.all().filter(active=True)
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication, ]
    permission_classes = []
    serializer_class = EmptySerializer
    pagination_class = CustomPagination
    filter_backends = (DynamicSearchFilter,)
    parser_classes = (MultiPartParser, JSONParser)

    serializer_classes = {
        'list': NodeSerializer,
        'retrieve': NodeSerializer
    }

    